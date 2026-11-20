"""Testes da leitura e gravação de arquivos (src/dados.py), usando arquivos temporários."""
import json

import pytest

from src import dados
from src.config import CARTOES_POR_PARTIDA


# --- Recorde ---------------------------------------------------------------

@pytest.fixture
def arquivo_recorde(tmp_path, monkeypatch):
    """Faz o módulo de dados usar um arquivo de recorde temporário (não mexe no real)."""
    caminho = tmp_path / "recorde.txt"
    monkeypatch.setattr(dados, "ARQUIVO_RECORDE", caminho)
    return caminho


def test_carregar_recorde_arquivo_inexistente(arquivo_recorde):
    """Sem arquivo, o recorde é 0."""
    assert dados.carregar_recorde() == 0


def test_carregar_recorde_arquivo_vazio(arquivo_recorde):
    """Arquivo vazio vale recorde 0."""
    arquivo_recorde.write_text("", encoding="utf-8")
    assert dados.carregar_recorde() == 0


def test_carregar_recorde_com_texto_invalido(arquivo_recorde):
    """Conteúdo que não é número vale recorde 0 (sem travar o jogo)."""
    arquivo_recorde.write_text("abc", encoding="utf-8")
    assert dados.carregar_recorde() == 0


def test_carregar_recorde_negativo_vira_zero(arquivo_recorde):
    """Um valor negativo no arquivo é tratado como 0."""
    arquivo_recorde.write_text("-5", encoding="utf-8")
    assert dados.carregar_recorde() == 0


def test_carregar_recorde_com_bom_e_quebra_de_linha_do_windows(arquivo_recorde):
    """Recorde salvo com BOM e quebra de linha do Windows (CRLF) deve ser lido corretamente."""
    arquivo_recorde.write_bytes(b"\xef\xbb\xbf120\r\n")
    assert dados.carregar_recorde() == 120


def test_carregar_recorde_valido(arquivo_recorde):
    """Deve ler o número salvo no arquivo."""
    arquivo_recorde.write_text("120\n", encoding="utf-8")
    assert dados.carregar_recorde() == 120


def test_salvar_recorde_maior_atualiza_o_arquivo(arquivo_recorde):
    """Pontuação maior que o recorde deve ser gravada e retornada."""
    arquivo_recorde.write_text("50", encoding="utf-8")
    assert dados.salvar_recorde(80) == 80
    assert dados.carregar_recorde() == 80


def test_salvar_recorde_menor_nao_altera_o_arquivo(arquivo_recorde):
    """Pontuação menor que o recorde não muda o arquivo; retorna o recorde atual."""
    arquivo_recorde.write_text("50", encoding="utf-8")
    assert dados.salvar_recorde(20) == 50
    assert dados.carregar_recorde() == 50


def test_salvar_recorde_sem_arquivo_cria_o_arquivo(arquivo_recorde):
    """Se o arquivo não existe, o primeiro recorde cria o arquivo."""
    assert dados.salvar_recorde(30) == 30
    assert arquivo_recorde.exists()


def test_salvar_recorde_pontuacao_negativa(arquivo_recorde):
    """Pontuação negativa deve gerar ValueError."""
    with pytest.raises(ValueError):
        dados.salvar_recorde(-1)


def test_salvar_recorde_tipo_invalido(arquivo_recorde):
    """Pontuação que não é inteiro deve gerar TypeError."""
    with pytest.raises(TypeError):
        dados.salvar_recorde("10")


def test_salvar_recorde_nao_deixa_arquivo_temporario(arquivo_recorde):
    """A gravação usa um arquivo temporário, que não pode sobrar na pasta."""
    dados.salvar_recorde(40)
    assert [arquivo.name for arquivo in arquivo_recorde.parent.iterdir()] == ["recorde.txt"]
    assert arquivo_recorde.read_text(encoding="utf-8") == "40\n"


def test_salvar_recorde_cria_a_pasta_se_nao_existir(tmp_path, monkeypatch):
    """Se a pasta do recorde não existir, ela é criada."""
    caminho = tmp_path / "nova_pasta" / "recorde.txt"
    monkeypatch.setattr(dados, "ARQUIVO_RECORDE", caminho)
    assert dados.salvar_recorde(10) == 10
    assert caminho.read_text(encoding="utf-8") == "10\n"


def test_salvar_recorde_igual_nao_reescreve_o_arquivo(arquivo_recorde):
    """Pontuação igual ao recorde não conta como novo recorde."""
    arquivo_recorde.write_text("50", encoding="utf-8")
    assert dados.salvar_recorde(50) == 50
    assert arquivo_recorde.read_text(encoding="utf-8") == "50"


# --- Cartões ---------------------------------------------------------------

@pytest.fixture
def arquivo_cartoes(tmp_path, monkeypatch):
    """Faz o módulo de dados usar um arquivo de cartões temporário."""
    caminho = tmp_path / "cartoes.json"
    monkeypatch.setattr(dados, "ARQUIVO_CARTOES", caminho)
    return caminho


def escrever_json(caminho, conteudo):
    """Escreve um conteúdo em formato JSON no arquivo informado."""
    caminho.write_text(json.dumps(conteudo), encoding="utf-8")


def test_carregar_cartoes_validos(arquivo_cartoes):
    """Deve carregar uma lista de cartões bem formados."""
    escrever_json(arquivo_cartoes, [{"texto": "a", "confiavel": True, "pista": "b"}])
    cartoes = dados.carregar_cartoes()
    assert len(cartoes) == 1
    assert cartoes[0]["texto"] == "a"


def test_carregar_cartoes_sem_campo_obrigatorio(arquivo_cartoes):
    """Cartão sem o campo 'pista' deve gerar erro."""
    escrever_json(arquivo_cartoes, [{"texto": "a", "confiavel": True}])
    with pytest.raises(ValueError):
        dados.carregar_cartoes()


def test_carregar_cartoes_confiavel_nao_booleano(arquivo_cartoes):
    """O campo 'confiavel' precisa ser true ou false."""
    escrever_json(arquivo_cartoes, [{"texto": "a", "confiavel": "sim", "pista": "b"}])
    with pytest.raises(ValueError):
        dados.carregar_cartoes()


def test_carregar_cartoes_texto_vazio(arquivo_cartoes):
    """Cartão com texto vazio deve gerar erro."""
    escrever_json(arquivo_cartoes, [{"texto": "  ", "confiavel": True, "pista": "b"}])
    with pytest.raises(ValueError):
        dados.carregar_cartoes()


def test_carregar_cartoes_item_que_nao_e_dicionario(arquivo_cartoes):
    """Cada cartão da lista precisa ser um dicionário."""
    escrever_json(arquivo_cartoes, ["texto solto"])
    with pytest.raises(ValueError):
        dados.carregar_cartoes()


def test_carregar_cartoes_pista_vazia(arquivo_cartoes):
    """Cartão com pista vazia deve gerar erro."""
    escrever_json(arquivo_cartoes, [{"texto": "a", "confiavel": True, "pista": ""}])
    with pytest.raises(ValueError):
        dados.carregar_cartoes()


def test_carregar_cartoes_conteudo_que_nao_e_lista(arquivo_cartoes):
    """O arquivo precisa conter uma lista de cartões."""
    escrever_json(arquivo_cartoes, {"texto": "a"})
    with pytest.raises(ValueError):
        dados.carregar_cartoes()


def test_carregar_cartoes_arquivo_salvo_com_bom(arquivo_cartoes):
    """Arquivo salvo com BOM (comum em editores do Windows) deve carregar normalmente."""
    conteudo = json.dumps([{"texto": "a", "confiavel": True, "pista": "b"}]).encode("utf-8")
    arquivo_cartoes.write_bytes(b"\xef\xbb\xbf" + conteudo)
    assert len(dados.carregar_cartoes()) == 1


def test_carregar_cartoes_json_malformado(arquivo_cartoes):
    """JSON com erro de sintaxe deve gerar ValueError (que o jogo trata com um aviso)."""
    arquivo_cartoes.write_text("[{ 'texto': 1 }", encoding="utf-8")
    with pytest.raises(ValueError):
        dados.carregar_cartoes()


def test_carregar_cartoes_arquivo_inexistente(arquivo_cartoes):
    """Arquivo inexistente deve gerar FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        dados.carregar_cartoes()


def test_cartoes_reais_nao_tem_textos_repetidos():
    """Nenhum texto de cartão deve aparecer duas vezes no arquivo real."""
    textos = [c["texto"].strip().lower() for c in dados.carregar_cartoes()]
    assert len(textos) == len(set(textos))


def test_cartoes_reais_cabem_na_tela():
    """Textos e pistas muito longos não cabem na área do cartão (limites do layout)."""
    for cartao in dados.carregar_cartoes():
        assert len(cartao["texto"]) <= 160
        assert len(cartao["pista"]) <= 160


def test_cartoes_reais_tem_exemplos_de_cada_tipo():
    """O jogo precisa de cartões confiáveis e suspeitos (pelo menos 5 de cada)."""
    cartoes = dados.carregar_cartoes()
    assert sum(1 for c in cartoes if c["confiavel"]) >= 5
    assert sum(1 for c in cartoes if not c["confiavel"]) >= 5


def test_arquivo_real_de_cartoes_tem_cartoes_suficientes_para_uma_partida():
    """O arquivo data/cartoes.json do jogo deve carregar e ter cartões para uma partida."""
    cartoes = dados.carregar_cartoes()
    assert len(cartoes) >= CARTOES_POR_PARTIDA
    assert any(c["confiavel"] for c in cartoes)
    assert any(not c["confiavel"] for c in cartoes)


def test_erro_informa_o_numero_do_cartao_e_o_campo_que_falta(arquivo_cartoes):
    """A mensagem de erro diz qual cartão tem problema e qual campo falta."""
    escrever_json(arquivo_cartoes, [
        {"texto": "a", "confiavel": True, "pista": "b"},
        {"texto": "c", "confiavel": False},
    ])
    with pytest.raises(ValueError) as erro:
        dados.carregar_cartoes()
    assert "cartão 2" in str(erro.value)
    assert "pista" in str(erro.value)


def test_validar_cartao_aceita_cartao_correto():
    """Um cartão bem formado não gera erro."""
    dados.validar_cartao({"texto": "a", "confiavel": False, "pista": "b"}, 1)


def test_validar_cartao_rejeita_pista_so_com_espacos():
    """Pista com apenas espaços conta como vazia."""
    with pytest.raises(ValueError):
        dados.validar_cartao({"texto": "a", "confiavel": True, "pista": "   "}, 1)
