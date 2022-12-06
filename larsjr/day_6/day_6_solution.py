def find_characters_processed_when_packet_found(signal: str, packet_size: int) -> int:
    for i in range(len(signal)):
        if len(set(signal[i : i + packet_size])) == packet_size:
            return i + packet_size
    return -1


if __name__ == "__main__":
    with open("input.txt", "r") as fp:
        signal = fp.read()

    characters_processed_part_1 = find_characters_processed_when_packet_found(
        signal, packet_size=4
    )
    print(f"Solution part 1: {characters_processed_part_1}")

    characters_processed_part_2 = find_characters_processed_when_packet_found(
        signal, packet_size=14
    )
    print(f"Solution part 2: {characters_processed_part_2}")
