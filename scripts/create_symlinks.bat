REM Copyright (C) 2019-2020 Intel Corporation
REM SPDX-License-Identifier: Apache-2.0
@echo off

if exist %1\deployment_tools\inference_engine (
    mklink /D %1\inference_engine %1\deployment_tools\inference_engine
)
if exist %1\deployment_tools\open_model_zoo\models\intel (
    mklink /D %1\deployment_tools\intel_models %1\deployment_tools\open_model_zoo\models\intel
    mklink /D %1\deployment_tools\open_model_zoo\intel_models %1\deployment_tools\open_model_zoo\models\intel
)
if exist %1\deployment_tools\open_model_zoo\tools\downloader (
    mklink /D %1\deployment_tools\tools\model_downloader %1\deployment_tools\open_model_zoo\tools\downloader
)
if exist %1\deployment_tools\open_model_zoo\demos (
    mklink /D %1\deployment_tools\inference_engine\demos %1\deployment_tools\open_model_zoo\demos
)
if exist %1\deployment_tools\open_model_zoo (
    mklink /D %1\deployment_tools\tools\post_training_optimization_toolkit\libs\open_model_zoo %1\deployment_tools\open_model_zoo
)


