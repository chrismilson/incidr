import re

# captures the ip address and the mask separately
CIDR_BLOCK_REGEX = re.compile(r"^(\d+)\.(\d+)\.(\d+)\.(\d+)\/(\d+)$")

def _popcount(n):
    result = 0
    while n:
        result += 1
        n &= n - 1
    return result

class CidrBlock:
    def __init__(self, base_ip, subnet_mask):
        self.base_ip = base_ip & subnet_mask
        self.subnet_mask = subnet_mask

    @staticmethod
    def from_string(cidr_block_str):
        match = CIDR_BLOCK_REGEX.search(cidr_block_str)
        if not match:
            raise Exception(f"Not a valid cidr block: {cidr_block_str}")

        match_numbers = list(map(int, match.groups()))
        ip_part = match_numbers[:4]
        subnet_part = match_numbers[4]

        if not (0 <= subnet_part <= 32):
            raise Exception(f"Invalid subnet part in cidr block: {cidr_block_str}")

        subnet_mask = 0xffffffff ^ ((1 << 32 - subnet_part) - 1)

        if not all(0 <= byte < 256 for byte in ip_part):
            raise Exception(f"Invalid IPv4 address in cidr block: {cidr_block_str}")

        base_ip = (ip_part[0] << 24) | (ip_part[1] << 16) | (ip_part[2] << 8) | ip_part[3]
        return CidrBlock(base_ip, subnet_mask)
        
    def __contains__(self, other):
        return self.base_ip == other.base_ip & self.subnet_mask

    def _ip_bytes(self):
        base_ip = self.base_ip
        return [(base_ip >> 24) & 0xff, (base_ip >> 16) & 0xff, (base_ip >> 8) & 0xff, base_ip & 0xff]

    def __str__(self):
        return ".".join(map(str, self._ip_bytes())) + f"/{_popcount(self.subnet_mask)}"

    # The cidr block that contains both self and other with minimum subnet size
    def __or__(self, other):
        base_ip = self.base_ip & other.base_ip
        subnet_mask = self.subnet_mask & other.subnet_mask
        while self.base_ip & subnet_mask != other.base_ip & subnet_mask:
            subnet_mask &= subnet_mask - 1

        return CidrBlock(base_ip, subnet_mask)

    def __eq__(self, other):
        return self.base_ip == other.base_ip and self.subnet_mask == other. subnet_mask

class CidrTree:
    def __init__(self, root=None, children=[]):
        self.root = root
        self.children = children

    def add(self, cidr: CidrBlock):
        if self.root and cidr == self.root:
            return

        # If the cidr belongs inside a child, add it
        for child in self.children:
            if cidr in child.root:
                child.add(cidr)
                return
        
        # gather all children that belong inside the block
        children = []
        siblings = []
        for child in self.children:
            if child.root in cidr:
                children.append(child)
            else:
                siblings.append(child)

        self.children = siblings
        self.children.append(CidrTree(cidr, children))
        
    def _str(self, depth):
        lines = []
        if depth >= 0:
            lines.append("\t" * depth + str(self.root))
        for child in self.children:
            lines.append(child._str(depth + 1))
        return "\n".join(lines)

    def __str__(self):
        return self._str(-1)

    def __contains__(self, cidr):
        return cidr in self.root
