REM Copyright (C) 2019-2020 Intel Corporation
REM SPDX-License-Identifier: Apache-2.0
@echo off
for /r "%1" %%F in (*requirements*.*) do (
  Echo.%%F | findstr /C:"post_training_optimization_toolkit" /C:"accuracy_checker" /C:"python3" /C:"python2" /C:"requirements_ubuntu">nul && (
    echo "Skip %%F"
    ) || (
        python -m pip install --no-cache-dir -r "%%F"
    )
)
exit /B 0