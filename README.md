# FastApi | pythônico
## Micro-serviços com framework web FastApi

### A construção de micro-serviços deste framework comparada ao spring é realmente rápida, não apenas em termos de documentação com o Swagger, mas na simplicidade de se criar os serviços em si.
Com apenas alguns comandos para instalar libs como <b>fastapi sqlalchemy asyncpg uvicorn psycopg2-binary guviconr</b>, alguns imports e você já consegue criar seus serviços.

E já temos a documentação dos serviços criados rápidamente criados e.g;

### <b>CODS</b>
<img src="https://i.imgur.com/T1fbcOo.png" width="400" />

### <b>REDOC</b>
<img src="https://i.imgur.com/nB8hb8b.png" width="400" />

## Atualização de libs de sqlalchemy para SQLModel
Ela por si implementa a sqlalchemy, tem algumas correções para se fazer dependendo da versão, mas ela suporta todas as libs anteriores. 
Seu uso é muito simples, não precisei utilizar schemas para mapear minhas entidas inboud ou outbound. Falando da injeção de depedência, o uso do banco de dados é bem explicito, praticamente sua instancia fica como parâmetro de sua rotina/api/escopo.

## Autenticação
JWT | Bearer | OAuth2PasswordBearer | jose - A construção de identificação e autorização foi bem simples sua construção e utilização, apenas injentando a dependência como parametro da rotina, ela por si só vai solicitar ao menos um usuário logado, extremamente rápido. Realizei também validações de alguns atributos com email a lib EmailStr. 

Após a autenticação, o swagger exigiu autenticação para utilização de chamadas.<hr>
<img src="https://i.imgur.com/eF28nAX.png" width="400" /><hr>

## [PEP 8](https://peps.python.org/pep-0008/)
As minhas primeiras impressões em relação ao spring é que o python é no minimo não verboso, o python é uma stack pra ser de certa forma objetiva e direta, não que o framework spring não seja, mas a rapidez com que configuramos, construímos e utilizamos os componentes é realmente incrivel.
A documentação sobre a elegibilidade, design e expressões que o guia de estilo pep 8 aborda é bem simples, ela aborda itens como espaçamentos, quantidade de caracteres por linha, quebra de linha, expressões, validações, palavras chaves, padrões como camelCase, vale a pena dar uma olhada.
Neste projeto fiz o uso do pylint para analisar e seguir a PEP o mais próximo possível, o pylint é uma das libs existêntes que faz uma analise estática de seu código-fonte de acordo com a documentação PEP 8, é praticamente o sonar do python rs, mas foi bem massante adequear o que eu ja havia construído. É legal você inserir essas validações numa esteira ci/cd, em um deos steps, utilize a analise statica de código com libs como essa.
