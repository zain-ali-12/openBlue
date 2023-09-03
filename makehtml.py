class HtmlCreator:
    def __init__(self):
        pass

    def create_tag(self, tagname, attributes='', data=''):
        tag_text = f'<{tagname} {attributes}>{data}<{tagname}/>'
        if tagname in ['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input' 'keygen', 'link', 'meta', 'param', 'source', 'track', 'wbr']:
            tag_text = tag_text[: - len(tagname) - 3]
        return tag_text


if __name__ == '__main__':
    tg = HtmlCreator()
    tg.create_tag('img', attributes='src="sadfasdf"')