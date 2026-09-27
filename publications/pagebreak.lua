function Header(el)
  if el.level == 2 then
    return {
      pandoc.RawBlock('openxml', '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'),
      pandoc.RawBlock('latex', '\\newpage\n'),
      el
    }
  end
end
