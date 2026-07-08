import time

print("START")

storage_size = 1_000_00
block_size = 4096


class Block:
    def __init__(self) -> None:
        self.content: list[str] = []

class INode:
    def __init__(self) -> None:
        self.blocks: list[Block] = []

class File:
    def __init__(self) -> None:
        self.inode = INode()
        self.created_at = time.time()

class FileSystem:
    def __init__(self) -> None:
        self.storage = [0] * storage_size
        self.files: dict[str,File] = {}

    def touch(self, filename) -> None:
        new_file = File()
        self.files[filename] = new_file

    def ls(self) -> list[str]:
        res = []
        res.extend(list(self.files.keys()))
        return res

    def cat(self, filename) -> str:
        contents = []
        blocks = self.files[filename].inode.blocks
        for i in range(len(blocks)):
            block_content = blocks[i].content
            contents.extend(block_content)
        return "".join(contents)

    def _content_to_blocks(self, content) -> list[Block]:
        blocks: list[Block] = []
        for i in range(0, len(content), block_size):
            upper_limit = min(len(content), i + block_size)
            new_block = Block()
            new_block.content = content[i:upper_limit]
            blocks.append(new_block)
        return blocks

    def write_to_file(self, filename, content) -> None:
        file_inode = self.files[filename].inode
        new_blocks = self._content_to_blocks(content)
        file_inode.blocks = new_blocks
        return None



fs = FileSystem()
assert fs.touch("somefile.log") == None
assert fs.ls() == ["somefile.log"]
assert fs.write_to_file("somefile.log", "hey") == None
assert fs.cat("somefile.log") == "hey", f"{fs.cat("somefile.log")}"
print("END")
