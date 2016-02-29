from fbtf import output, Foobar

f = Foobar()

path = f['path']

start_with_http = path.left(7).stricmp('http://')
strip_http = path.right(path.len() - 7)

# get rid ef leading http://, then get rid of any port number
domain = strip_http.left(strip_http.strchr('/') - 1)
domain_no_port = domain.left(domain.strchr(':') - 1)

# helpers
domain_no_port_first_dot = domain_no_port.strchr('.')
domain_no_port_last_dot = domain_no_port.strrchr('.')
domain_right_part = domain_no_port.right(domain_no_port.len() - domain_no_port_last_dot)

# TODO: the domain shortening logic is a huge hack, could be better
# only shorten domain if the right most part isn't a TLD (at a guess)
shortened_domain = f.ifequal(domain_right_part.len(), 2,
                             domain_no_port,
                             domain_no_port.right(domain_no_port.len() - domain_no_port_first_dot))

# try to shorten the domain to get rid of subdomains
shortened_if_domain = f.ifequal(domain_no_port_last_dot, domain_no_port_first_dot,
                                domain_no_port,
                                shortened_domain)

# main body
script = f.if_(start_with_http, shortened_if_domain, path)

if __name__ == '__main__':
    # print(domain_no_port.output())
    print(output(script))

    # $if($stricmp($left(%path%,7),'http://'),$left($put(v0,$left($put(v1,$right(%path%,$sub($len(%path%),7))),$sub($strchr($get(v1),'/'),1))),$sub($strchr($get(v0),':'),1)),%path%)
