-- Source-addressed Mermaid cache. Each publishing job has its own working dir.
-- Caption changes cannot reuse a diagram for changed Mermaid source text.
local function valid_png(path)
  local file = io.open(path, "rb")
  if not file then return false end
  local signature = file:read(8)
  file:close()
  return signature == "\137PNG\13\10\26\10"
end

function CodeBlock(block)
  if not block.classes:includes("mermaid") then return nil end
  local digest = pandoc.utils.sha1(block.text)
  local source = "temp_mermaid_" .. digest .. ".mmd"
  local output = "images/mermaid_" .. digest .. ".png"
  if not valid_png(output) then
    local file = assert(io.open(source, "wb"))
    file:write(block.text)
    file:close()
    local command = string.format(
      'mmdc -i "%s" -o "%s" -t default -b transparent -p "internal/puppeteer-config.json"',
      source, output
    )
    local success = os.execute(command)
    os.remove(source)
    if not success or not valid_png(output) then
      error("Mermaid rendering failed for source hash " .. digest .. "; verify mmdc/browser installation and diagram syntax.")
    end
  end
  return pandoc.Para({pandoc.Image({}, output)})
end
