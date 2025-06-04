# Using OpenVINO™ Toolkit containers with NPU accelerators

To use the NPU (Neural Processing Unit) Driver inside a container:
- Ensure that the corresponding firmware package `intel-fw-npu` is installed on the host. 
- Add NPU device to the container, for example, by using the argument `--device=/dev/accel/accel0` when running your container. 

See [NPU Driver release page](https://github.com/intel/linux-npu-driver/releases) for setup details.

## NPU device recovery

There is a known issue with NPU device recovery in the current NPU Driver.
Starting from NPU Linux driver release v1.13.0, a new NPU recovery behavior has been introduced. 
Corresponding changes in Ubuntu kernels are expected with new kernel releases. 

For more details, see the [known issue page](https://github.com/intel/linux-npu-driver/issues/87).

### Troubleshooting 

If inference on the NPU crashes, you can manually reload the driver by running this command in the terminal: 

```
sudo rmmod intel_vpu
sudo modprobe intel_vpu
```

## See also

[Intel® NPU Driver GitHub](https://github.com/intel/linux-npu-driver)

[Working with OpenVINO Containers](containers.md)

[Install Intel® Distribution of OpenVINO™ Toolkit From a Docker Image](https://docs.openvino.ai/2025/get-started/install-openvino/install-openvino-docker-linux.html)
