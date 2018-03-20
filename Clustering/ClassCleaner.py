#https://gitlab.com/gabrielsarmento/PythonTextFilter

class TextCleaner:

    def __init__(self):
        pass


    def filter (self,body):
        body = str(body)
        import re
        regex = [

	    [r'<!--[^*]*-->',' '],
            [r'`.+?`',' '],

            
            [r'<code>.+?</code>',' '],
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
"""
   def filterNoRegex(self, body):

       body = str(body)
       tags = [
            '<div class=""snippet-code"">'
           ]
       posicaoInicialDoCodigo = [
"""

if __name__ == '__main__':
    from pprint import pprint
    f = PostCleaner()
    post = input()
    output = f.filter(post)
    pprint(output)
