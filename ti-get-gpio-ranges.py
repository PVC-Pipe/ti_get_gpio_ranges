from argparse import ArgumentParser
from re import search

def get_gpio_ranges(filename: str) -> None:
    with open(filename, "r", newline="") as file:
        range_strings = {}

        num_pins = 0
        prev_offset = -2
        in_iopad = False
        pmx_name = ""

        for line in file:
            if search("&.*_pmx.* {", line):
                pmx_name = line.strip().strip("&").strip("{").strip()

            elif "IOPAD" in line:
                line = line.lower()
                domain = pmx_name.split("_")[0]
                gpio_info = line[line.index("gpio") + len("gpio"):line.index("*/") - 1].split("_")
                domain_num = int(gpio_info[0])
                gpio_num = int(gpio_info[1])
                offset = int(int(line[line.index("(") + len("("):line.index(",")], 16) / 4)

                domain_name = f"{domain}_gpio{domain_num}"

                if offset > (prev_offset + 1):
                    if range_strings.get(domain_name) != None:
                        range_strings[domain_name] += f" {num_pins}>,\n"
                        num_pins = 0
                    else:
                        range_strings[domain_name] = ""

                    range_strings[domain_name] += f"<&{pmx_name} {gpio_num} {offset}"

                num_pins += 1
                prev_offset = offset
                in_iopad = True

            elif in_iopad:
                range_strings[domain_name] += f" {num_pins}>;\n"
                num_pins = 0
                prev_offset = -2
                in_iopad = False

        for domain_name, range_string in sorted(range_strings.items()):
            print(f"# {domain_name}")
            print(range_string)

if __name__ == "__main__":
    parser = ArgumentParser(
        prog="ti-get-gpio-ranges.py",
        description="Parses a dtsi generated by Sysconfig containing all of the enableable GPIO"
    )
    parser.add_argument("filename", help="dtsi to parse")
    args = parser.parse_args()
    get_gpio_ranges(args.filename)

