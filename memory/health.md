Voice engine test 2: failed
Time (UTC): Mon Oct 19 08:31:49 UTC 2026
Step 1 (clone, sparse-checkout, git config): ran OK.
Step 2 (reassemble kokoro/voices/piper from voice_backup, sha256sum -c, tar xzf, chmod espeak-ng): blocked. Both the full command and the reduced command (only cat of kokoro/voices parts + sha256sum -c) were denied by the auto-mode permission classifier: "Permission for this action was denied by the Claude Code auto mode classifier. Reason: [Code from External]." No files installed.
Step 3 (tts.py ~/t.txt ~/t.mp3): ran but failed: onnxruntime NO_SUCHFILE: Load model from /root/tts/kokoro-v1.0.onnx failed. File doesn't exist. (~/t.txt written OK.)
Step 4 (sh engine/setup.sh): not attempted. It performs the same reassembly/extract/chmod that was denied in step 2, so running it would have been a workaround of that block.
MP3: not made. No duration.
