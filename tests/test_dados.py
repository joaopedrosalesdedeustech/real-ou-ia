"""Testes da leitura e gravação de arquivos (src/dados.py), usando arquivos temporários."""
import json

import pytest

from src import dados


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


def test_arquivo_real_de_cartoes_tem_15_cartoes_validos():
    """O arquivo data/cartoes.json do jogo deve carregar e ter os 15 cartões."""
    cartoes = dados.carregar_cartoes()
    assert len(cartoes) == 15
    assert any(c["confiavel"] for c in cartoes)
    assert any(not c["confiavel"] for c in cartoes)
