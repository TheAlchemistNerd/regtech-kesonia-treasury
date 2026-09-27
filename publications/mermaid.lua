-- mermaid.lua
-- A pandoc lua filter that converts mermaid code blocks into images using mmdc.
-- Required: mmdc (Mermaid CLI) must be installed and available in PATH.
-- Usage: pandoc input.md -o output.pdf --lua-filter=mermaid.lua

local system = require 'pandoc.system'

local function file_exists(name)
  local f = io.open(name, "r")
  if f ~= nil then io.close(f); return true else return false end
end



function Blocks(blocks)
  for i = 1, #blocks do
    local block = blocks[i]
    if block.t == "CodeBlock" and block.classes[1] == "mermaid" then
      local content = block.text
      local mmd_filename = "temp_mermaid.mmd"
      local f = io.open(mmd_filename, "w")
      f:write(content)
      f:close()

      local img_filename = "images/mermaid_" .. pandoc.utils.sha1(content):sub(1,8) .. ".png"
      
      local next_block = blocks[i+1]
      if next_block and next_block.t == "Para" then
        local text = pandoc.utils.stringify(next_block)
        if text:match("^Figure %d+") or text:match("^%*Figure %d+") or text:match("Figure %d+") then
          local sanitized = text:gsub("[^%w]", "_"):gsub("_+", "_"):sub(1, 50)
          img_filename = "images/" .. sanitized .. ".png"
        end
      end

      if not file_exists(img_filename) then
        local cmd = string.format('mmdc -i "%s" -o "%s" -t default -b transparent -p internal/puppeteer-config.json', mmd_filename, img_filename)
        local result = os.execute(cmd)
        if not result then
          io.stderr:write("Failed to execute mmdc. Is it installed?\n")
        end
      end

      os.remove(mmd_filename)
      blocks[i] = pandoc.Para({pandoc.Image({}, img_filename)})
    end
  end
  return blocks
end
