from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import operator_benchmark as op_bench
import torch


"""Microbenchmarks for channel_shuffle operator."""


# Configs for PT channel_shuffle operator
channel_shuffle_long_configs = op_bench.cross_product_configs(
    batch_size=[1, 2, 4, 8, 16],
    channels_per_group=[16, 32, 64, 128],
    height=[16, 32, 64, 128],
    width=[16, 32, 64, 128],
    groups=[2, 4, 8, 16],
    channel_last=[True, False],
    tags=["long"]
)


channel_shuffle_short_configs = op_bench.config_list(
    attr_names=["batch_size", "channels_per_group", "height", "width", "groups"],
    attrs=[
        [2, 16, 16, 16, 2],
        [2, 32, 32, 32, 2],
        [4, 32, 32, 32, 4],
        [4, 64, 64, 64, 4],
        [8, 64, 64, 64, 8],
        [8, 128, 128, 128, 8],
        [16, 64, 64, 64, 16],
        [16, 128, 128, 128, 16],
        [16, 256, 256, 256, 16],
    ],
    cross_product_configs={
        "channel_last": [True, False],
    },
    tags=["short"]
)


class ChannelSHuffleBenchmark(op_bench.TorchBenchmarkBase):
    def init(self, batch_size, channels_per_group, height, width, groups, channel_last):
        self.groups = groups
        channels = channels_per_group * groups
        data_shape = (batch_size, channels, height, width)
        self.input_data = torch.rand(data_shape)
        if channel_last:
            self.input_data = self.input_data.contiguous(memory_format=torch.channels_last)
        self.set_module_name('channel_shuffle')

    def forward(self):
        return torch.channel_shuffle(self.input_data, self.groups)


op_bench.generate_pt_test(channel_shuffle_short_configs + channel_shuffle_long_configs,
                          ChannelSHuffleBenchmark)


if __name__ == "__main__":
    op_bench.benchmark_runner.main()
