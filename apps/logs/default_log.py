# coding: utf-8

from __future__ import unicode_literals


def body(lang):
    log_pt = '<p><strong>Olá, bem-vindo(a) ao logd.me!</strong></p>\n' \
        '<p>Este é o seu diário <span class="hashtag">#pessoal</span>, onde você pode salvar as ' \
        'coisas ' \
        'que aconteceram ou ainda vão acontecer, registrar eventos importantes, reuniões, ' \
        'telefonemas, ' \
        'qualquer coisa ... para que você possa facilmente lembrar sempre que precisar.</p>\n' \
        '<p>Nós construímos este aplicativo para ser simples e rápido, veja algumas ' \
        'características principais:</p>\n' \
        '<ul>\n' \
        '<li>Editor de texto rico</li>\n' \
        '<li>@citações para pessoas e empresas</li>\n' \
        '<li>Tags</li>\n' \
        '<li>Atalhos do teclado</li>\n' \
        '<li>Busca extremamente simples e rápida por:</li>\n' \
        '<ul>\n' \
        '<li>Conteúdos</li>\n' \
        '<li>Tags</li>\n' \
        '<li>Datas</li>\n' \
        '<li>Destaques (pesquise por "!!!")</li>\n' \
        '<li>@citações</li>\n' \
        '<li>Tags <span class="hashtag">#bem-vindo</span> <span class="hashtag">#logd</span>' \
        '</li>\n' \
        '</ul>\n' \
        '</ul>\n' \
        '<p>Aqui estão algumas pessoas de exemplo, como ' \
        '<span class="hl_mention_person" data-id="0">' \
        'John Doe</span>&nbsp;que não é ninguém e ' \
        '<span class="hl_mention_person" data-id="0">Gill Bates' \
        '</span>&nbsp;que trabalha na ' \
        '<span class="hl_mention_company" data-id="0">ACME Corporation' \
        '</span>, tudo em uma categoria <span class="hashtag">#inbox</span> padrão para você ' \
        'começar. ' \
        'Você pode excluir esses caras mais tarde.</p>\n' \
        '<blockquote>\n' \
        '<p><strong><span class="hashtag">#Dicas</span> rápidas:</strong></p>\n' \
        '<p>Digite \'@\', no editor, para exibir sugestões de citações<br>Digite \'#\', ' \
        'no editor, para ' \
        'adicionar uma tag<br>Digite \'/\' para focar na entrada de pesquisa<br>Digite \'esc\' ' \
        'para limpar ' \
        'a pesquisa<br>Procure por \'!!!\' para filtrar registros destacados</p>' \
        '</blockquote>' \
        '<p>Espero que você goste, aproveite!<br><strong>equipe do logd.me</strong></p></p>'

    log_en = '<p><strong>Hi there, welcome to logd.me!</strong></p>\n' \
        '<p>This is your <span class="hashtag">#personal</span> life log, where you can ' \
        'save things that happened or will happen, register important events, meetings, ' \
        'phone calls, anything... so you can easily remind whenever you need.</p>\n' \
        '<p>We built this app to be simple and fast, these are some core features:</p>\n' \
        '<ul>\n' \
        '<li>Rich text editor</li>\n' \
        '<li>@mentions for people and companies</li>\n' \
        '<li>Tags</li>\n' \
        '<li>Keyboard shortcuts</li>\n' \
        '<li>Extremily easy and fast fuzzy search by:</li>\n' \
        '<ul>\n' \
        '<li>Contents</li>\n' \
        '<li>Tags</li>\n' \
        '<li>Dates</li>\n' \
        '<li>Highlights (search for "!!!")</li>\n' \
        '<li>@mentions</li>\n' \
        '<li>Tags <span class="hashtag">#welcome</span> ' \
        '<span class="hashtag">#logd</span></li>\n' \
        '</ul>\n' \
        '</ul>\n' \
        '<p>Here are some sample people, like ' \
        '<span class="hl_mention_person" data-id="0">John Doe</span>&nbsp;who is ' \
        'nobody and <span class="hl_mention_person" data-id="0">Gill Bates</span>&nbsp;' \
        'who works at <span class="hl_mention_company" data-id="0">ACME Corporation</span>, ' \
        'all in a default <span class="hashtag">#inbox</span> category for you to get started. ' \
        'You can delete those guys later.</p>\n' \
        '<blockquote>\n' \
        '<p><strong>Quick <span class="hashtag">#tips</span>:</strong></p>\n' \
        '<p>Type \'@\', in editor, to bring up mentions suggestions<br>Type \'#\', in editor, ' \
        'to add a Tag<br>Type \'/\' to focus at search input<br>Type \'esc\' to clear search' \
        '<br>Search for \'!!!\' to filter highlighted logs</p>\n' \
        '</blockquote>\n' \
        '<p>Hope you like it, enjoy!<strong><br></strong><strong>logd.me Team</strong></p>'

    if lang == "pt-br":
        return log_pt

    if lang == "en-us":
        return log_en

    return "Language not found!"
