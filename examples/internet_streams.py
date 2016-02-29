from foobar import Foobar
from output import output

f = Foobar()

path = f['path']

start_with_http = path.left(7).stricmp('http://')
strip_http = f.memoize(path.right(path.len() - 7))

domain = f.memoize(strip_http.left(strip_http.strchr('/') - 1))
domain_no_port = domain.left(domain.strchr(':') - 1)

script = f.if_(start_with_http, domain_no_port, path)

if __name__ == '__main__':
    # print(domain_no_port.output())
    print(output(script))
    # $if($stricmp($left(%path%,7),'http://'),$left($put(v1,$right(%path%,$sub($len(%path%),7))),$sub($strchr($get(v1),'/'),1)),%path%)
    # $if($stricmp($left(%path%,7),'http://'),$left($put(v1,$right(%path%,$sub($len(%path%),7))),$sub($strchr($get(v1),'/'),1)),%path%)

