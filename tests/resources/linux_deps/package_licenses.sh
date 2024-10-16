# -*- coding: utf-8 -*-
# Copyright (C) 2021-2022 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
apt update
apt install -y --no-install-recommends git ca-certificates

git clone https://github.com/daald/dpkg-licenses.git /tmp/dpkg-licenses --depth 1

/tmp/dpkg-licenses/dpkg-licenses -c | awk -F ',' '{print $2"\n"$6"\n"}' | tr -d '"' > /tmp/logs/packages.log