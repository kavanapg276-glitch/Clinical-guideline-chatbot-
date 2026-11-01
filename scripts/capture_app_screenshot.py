"""Capture screenshot of running Streamlit app using Chrome DevTools Protocol (CDP)."""

import base64
import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any, cast

import websocket

REPO_ROOT = Path(__file__).resolve().parent.parent
SCREENSHOT_PATH = REPO_ROOT / "docs" / "screenshots" / "app_sidebar_clean.png"
SCREENSHOT_PATH.parent.mkdir(parents=True, exist_ok=True)

CHROME_PATH = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
VENV_STREAMLIT = REPO_ROOT / ".venv" / "Scripts" / "streamlit.exe"

message_counter = 0


def call_cdp(
    ws: websocket.WebSocket,
    method: str,
    params: dict[str, Any] | None = None,
    timeout: float = 30.0,
) -> dict[str, Any]:
    global message_counter
    message_counter += 1
    req_id = message_counter
    payload: dict[str, Any] = {"id": req_id, "method": method}
    if params:
        payload["params"] = params
    ws.send(json.dumps(payload))
    t_end = time.time() + timeout
    while time.time() < t_end:
        raw = ws.recv()
        data = json.loads(raw)
        if data.get("id") == req_id:
            return cast(dict[str, Any], data)
    raise TimeoutError(f"CDP call {method} timed out")


def main() -> None:
    print("[1] Starting Streamlit process...")
    cmd = [
        str(VENV_STREAMLIT),
        "run",
        "frontend/app.py",
        "--server.headless=true",
        "--server.port=8501",
        "--server.address=127.0.0.1",
    ]
    st_proc = subprocess.Popen(
        cmd,
        cwd=str(REPO_ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    url = "http://127.0.0.1:8501"
    ready = False
    print("[2] Waiting for Streamlit server on 127.0.0.1:8501...")
    for _ in range(35):
        time.sleep(1)
        try:
            with urllib.request.urlopen(f"{url}/_stcore/health", timeout=1) as resp:
                if resp.status == 200:
                    ready = True
                    break
        except Exception:
            pass

    if not ready:
        print("Streamlit failed to reach health status within 35s")
        st_proc.terminate()
        sys.exit(1)

    print("[3] Launching Chrome directly navigated to URL on port 9222...")
    chrome_proc = subprocess.Popen(
        [
            str(CHROME_PATH),
            "--headless=new",
            "--disable-gpu",
            "--remote-debugging-port=9222",
            "--window-size=1280,950",
            url,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    ws_url = None
    for _ in range(20):
        time.sleep(0.5)
        try:
            with urllib.request.urlopen("http://127.0.0.1:9222/json", timeout=1) as resp:
                data = json.loads(resp.read().decode())
                for target in data:
                    print("  target found:", target.get("type"), target.get("url"))
                    if target.get("type") == "page":
                        ws_url = target.get("webSocketDebuggerUrl")
                        break
                if ws_url:
                    break
        except Exception:
            pass

    if not ws_url:
        print("Failed to get Chrome CDP WebSocket URL")
        chrome_proc.terminate()
        st_proc.terminate()
        sys.exit(1)

    print(f"[4] Connecting to Chrome CDP at {ws_url}...")
    ws = websocket.create_connection(ws_url, timeout=60)

    call_cdp(ws, "Page.enable")
    call_cdp(ws, "Runtime.enable")

    # Poll DOM until .patient-card is rendered (orchestrator index load takes ~15-20s)
    print("[6] Waiting for .patient-card and Streamlit components to mount...")
    card_found = False
    for i in range(45):
        time.sleep(1)
        check_expr = "Boolean(document.querySelector('.patient-card'))"
        res = call_cdp(ws, "Runtime.evaluate", {"expression": check_expr, "returnByValue": True})
        if res.get("result", {}).get("result", {}).get("value") is True:
            card_found = True
            print(f"Mounted at second {i + 1}!")
            break
        if (i + 1) % 5 == 0:
            title_res = call_cdp(
                ws, "Runtime.evaluate", {"expression": "document.title", "returnByValue": True}
            )
            print(
                f"  .. waiting (page title: {title_res.get('result', {}).get('result', {}).get('value')})"
            )

    print(f"Patient card element found: {card_found}")

    # Inspect text of the patient card
    text_res = call_cdp(
        ws,
        "Runtime.evaluate",
        {
            "expression": "document.querySelector('.patient-card') ? document.querySelector('.patient-card').innerText : 'NOT FOUND'",
            "returnByValue": True,
        },
    )
    card_text = text_res.get("result", {}).get("result", {}).get("value")
    print(f"Patient card innerText:\n{card_text}\n")

    # Check if any pre or code elements exist inside .patient-card
    check_code = "Boolean(document.querySelector('.patient-card code, .patient-card pre'))"
    res_code = call_cdp(ws, "Runtime.evaluate", {"expression": check_code, "returnByValue": True})
    has_code = res_code.get("result", {}).get("result", {}).get("value")
    print(f"Raw code/pre tags inside patient card: {has_code}")

    # Wait an extra 2 seconds for CSS animations and fonts to settle
    time.sleep(2)

    # Capture Screenshot
    print("[7] Capturing screenshot via CDP Page.captureScreenshot...")
    shot_res = call_cdp(ws, "Page.captureScreenshot", {"format": "png"})
    b64_data = shot_res.get("result", {}).get("data", "")
    if b64_data:
        SCREENSHOT_PATH.write_bytes(base64.b64decode(b64_data))
        print(f"Saved screenshot: {SCREENSHOT_PATH} ({SCREENSHOT_PATH.stat().st_size} bytes)")
    else:
        print("Failed to capture screenshot data")

    ws.close()
    chrome_proc.terminate()
    st_proc.terminate()
    try:
        st_proc.wait(timeout=5)
    except Exception:
        st_proc.kill()
    print("Done!")


if __name__ == "__main__":
    main()
