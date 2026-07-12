-- mermaid.lua
-- A pandoc lua filter that converts mermaid code blocks into images using mmdc.
-- Required: mmdc (Mermaid CLI) must be installed and available in PATH.
-- Usage: pandoc input.md -o output.pdf --lua-filter=mermaid.lua

local system = require 'pandoc.system'

local function file_exists(name)
  local f = io.open(name, "r")
  if f ~= nil then io.close(f); return true else return false end
end

function CodeBlock(block)
  if block.classes[1] == "mermaid" then
    local content = block.text
    -- Create temporary file for mermaid code
    local mmd_filename = "temp_mermaid.mmd"
    local f = io.open(mmd_filename, "w")
    f:write(content)
    f:close()

    -- Generate a unique image filename based on content hash
    local img_filename = "images/mermaid_" .. pandoc.utils.sha1(content):sub(1,8) .. ".png"

    if not file_exists(img_filename) then
      -- Call mmdc to generate the image
      local cmd = string.format('mmdc -i "%s" -o "%s" -t default -b transparent -p internal/puppeteer-config.json', mmd_filename, img_filename)
      local result = os.execute(cmd)
      if not result then
        io.stderr:write("Failed to execute mmdc. Is it installed?\n")
        os.remove(mmd_filename)
        return block
      end
    end

    os.remove(mmd_filename)
    
    -- Replace code block with the generated image
    return pandoc.Para({pandoc.Image({}, img_filename)})
  end
end
