#https://gitlab.com/gabrielsarmento/PythonTextFilter
#adicionado algumas expressões regulares

class TextCleaner:

    def __init__(self):
        pass


    def filter (self,body):
        body = str(body)
        import re
        regex = [
			[r'(www\.|http[s]:).+(\.[0-9A-Za-z/]+)',''],#remove links
			[r'[\d+]',''],
			[r'[\*\+\-:;()]',' '],
			[r'<code>[^*]*?</code>',' '],#funcionando
			[r'</?[apredivhs].*?>',' '],
			[r'\s+?',' '],
			

            [r'<[^>]+>\s+(?=<)|<[^>]+>',''],
            [r'&#xA;',' '],
            [r';','.'],
            [r'[\]\[\(\)]',' '],
            [r' +',' '],
            [r' \.','.'],
            [r' *[\'\"], *',''],
            [r' $',''],
            [r'^ [\'"]',''],
            [r'\\','']
            ]

        for r in regex:
            body = re.sub(r[0],r[1],body)

        return body

if __name__ == '__main__':
    from pprint import pprint
    f = PostCleaner()
    post = input()
    output = f.filter(post)
    pprint(output)
