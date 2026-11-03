from atlas_node.probe import MIB, parse_nvidia_smi


def test_parse():
    gpus = parse_nvidia_smi("NVIDIA GeForce RTX 3060, 12288, 11500\nbasura\n")
    assert len(gpus) == 1 and gpus[0].vram_total_bytes == 12288 * MIB
