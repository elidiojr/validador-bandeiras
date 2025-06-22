#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validador de Bandeiras de Cartão de Crédito
===========================================

Este programa valida números de cartão de crédito usando o algoritmo Luhn
e identifica a bandeira do cartão (Visa, Mastercard, Elo, etc.).

Suporta as principais bandeiras brasileiras e internacionais:
- Visa
- Mastercard
- American Express
- Elo (bandeira brasileira)
- Hipercard (bandeira brasileira)
- Diners Club
- Discover
- JCB
- Aura
- Maestro

Autor: Gerado por IA
Data: 2025
"""

import re
from typing import Optional, Dict, Any


class ValidadorCartaoCredito:
    """
    Classe para validar números de cartão de crédito e identificar suas bandeiras.
    Implementa o algoritmo Luhn e padrões de bandeiras nacionais e internacionais.
    """

    def __init__(self):
        # Padrões regex para identificação de bandeiras
        self.padroes_bandeiras = {
            'visa': r'^4[0-9]{12}(?:[0-9]{3})?$',
            'mastercard': r'^5[1-5][0-9]{14}$|^2[2-7][0-9]{14}$',
            'amex': r'^3[47][0-9]{13}$',
            'elo': r'^(4011(78|79)|43(1274|8935)|45(1416|7393|763[12])|50(4175|6699|67[0-6][0-9]|677[0-8]|9[0-8][0-9]{2}|99[0-8][0-9]|999[0-9])|627780|63(6297|6368|6369)|65(0(0(3[1-3]|[5-9])|4[0-9]|5[0-1])|4(0[5-9]|[1-3][0-9]|8[5-9]|9[0-9])|5([0-2][0-9]|3[0-8]|4[1-9]|[5-8][0-9]|9[0-8])|7(0[0-9]|1[0-8]|2[0-7])|9(0[1-9]|[1-6][0-9]|7[0-8]))|16(5[2-9]|[6-7][0-9])|50(0[0-9]|1[0-9]|2[1-9]|[3-4][0-9]|5[0-8]))$',
            'hipercard': r'^(606282\d{10}(\d{3})?|3841\d{15})$',
            'diners': r'^3(?:0[0-5]|[68][0-9])[0-9]{11}$',
            'discover': r'^6(?:011|5[0-9]{2})[0-9]{12}$',
            'jcb': r'^(?:2131|1800|35\d{3})\d{11}$',
            'aura': r'^5078\d{2}\d{2}\d{11}$',
            'maestro': r'^(?:5[0678]\d\d|6304|6390|67\d\d)\d{8,15}$'
        }

        # Nomes das bandeiras em português
        self.nomes_bandeiras = {
            'visa': 'Visa',
            'mastercard': 'Mastercard',
            'amex': 'American Express',
            'elo': 'Elo',
            'hipercard': 'Hipercard',
            'diners': 'Diners Club',
            'discover': 'Discover',
            'jcb': 'JCB',
            'aura': 'Aura',
            'maestro': 'Maestro'
        }

    def limpar_numero(self, numero: str) -> str:
        """
        Remove espaços, hífens e outros caracteres não numéricos do número do cartão.

        Args:
            numero: Número do cartão com ou sem formatação

        Returns:
            str: Número limpo contendo apenas dígitos
        """
        return re.sub(r'[^0-9]', '', str(numero))

    def validar_luhn(self, numero: str) -> bool:
        """
        Implementa o algoritmo Luhn para validar números de cartão de crédito.

        O algoritmo Luhn foi desenvolvido por Hans Peter Luhn em 1954 e é usado
        para detectar erros de digitação em números de cartão de crédito.

        Args:
            numero: Número do cartão de crédito como string

        Returns:
            bool: True se o número for válido pelo algoritmo Luhn, False caso contrário
        """
        # Limpar o número
        numero = self.limpar_numero(numero)

        # Verificar se o número contém apenas dígitos
        if not numero.isdigit():
            return False

        # Converter para lista de inteiros
        digitos = [int(d) for d in numero]

        # Remover o último dígito (check digit)
        check_digit = digitos.pop()

        # Reverter os dígitos restantes
        digitos.reverse()

        # Dobrar dígitos em índices pares (começando do 0)
        for i in range(0, len(digitos), 2):
            digitos[i] *= 2
            # Se o resultado for maior que 9, subtrair 9
            if digitos[i] > 9:
                digitos[i] -= 9

        # Adicionar o check digit de volta
        digitos.append(check_digit)

        # Calcular a soma total
        soma_total = sum(digitos)

        # Verificar se é divisível por 10
        return soma_total % 10 == 0

    def identificar_bandeira(self, numero: str) -> Optional[str]:
        """
        Identifica a bandeira do cartão baseada no número.

        Args:
            numero: Número do cartão de crédito

        Returns:
            str: Nome da bandeira ou None se não identificada
        """
        numero = self.limpar_numero(numero)

        # Verificar cada padrão de bandeira
        for bandeira, padrao in self.padroes_bandeiras.items():
            if re.match(padrao, numero):
                return self.nomes_bandeiras[bandeira]

        return None

    def validar_cartao(self, numero: str) -> Dict[str, Any]:
        """
        Valida completamente um número de cartão de crédito.

        Args:
            numero: Número do cartão de crédito

        Returns:
            dict: Dicionário com resultado da validação contendo:
                - numero_original: Número como foi fornecido
                - numero_limpo: Número apenas com dígitos
                - valido_luhn: Se passou na validação Luhn
                - bandeira: Nome da bandeira identificada
                - valido_completo: Se é válido e tem bandeira identificada
                - comprimento: Número de dígitos
                - mensagem: Mensagem descritiva do resultado
        """
        numero_limpo = self.limpar_numero(numero)

        resultado = {
            'numero_original': str(numero),
            'numero_limpo': numero_limpo,
            'valido_luhn': False,
            'bandeira': None,
            'valido_completo': False,
            'comprimento': len(numero_limpo),
            'mensagem': ''
        }

        # Verificar se o número contém apenas dígitos após limpeza
        if not numero_limpo.isdigit():
            resultado['mensagem'] = 'Número contém caracteres inválidos'
            return resultado

        # Verificar comprimento válido
        if len(numero_limpo) < 13 or len(numero_limpo) > 19:
            resultado['mensagem'] = 'Comprimento inválido (deve ter entre 13 e 19 dígitos)'
            return resultado

        # Validar com algoritmo Luhn
        resultado['valido_luhn'] = self.validar_luhn(numero_limpo)

        # Identificar bandeira
        resultado['bandeira'] = self.identificar_bandeira(numero_limpo)

        # Determinar se é completamente válido
        resultado['valido_completo'] = resultado['valido_luhn'] and resultado['bandeira'] is not None

        # Definir mensagem de status
        if resultado['valido_completo']:
            resultado['mensagem'] = f'Cartão válido - Bandeira: {resultado["bandeira"]}'
        elif resultado['valido_luhn'] and resultado['bandeira'] is None:
            resultado['mensagem'] = 'Número válido pelo algoritmo Luhn, mas bandeira não identificada'
        elif not resultado['valido_luhn'] and resultado['bandeira'] is not None:
            resultado['mensagem'] = f'Bandeira identificada ({resultado["bandeira"]}), mas número inválido pelo algoritmo Luhn'
        else:
            resultado['mensagem'] = 'Número inválido'

        return resultado

    def formatar_numero(self, numero: str, bandeira: Optional[str] = None) -> str:
        """
        Formata o número do cartão de acordo com a bandeira.

        Args:
            numero: Número do cartão
            bandeira: Nome da bandeira (opcional)

        Returns:
            str: Número formatado
        """
        numero = self.limpar_numero(numero)

        if not bandeira:
            bandeira = self.identificar_bandeira(numero)

        # Formatação específica por bandeira
        if bandeira == 'American Express':
            # Amex: XXXX-XXXXXX-XXXXX
            if len(numero) == 15:
                return f"{numero[:4]}-{numero[4:10]}-{numero[10:]}"
        elif bandeira == 'Diners Club':
            # Diners: XXXX-XXXXXX-XXXX
            if len(numero) == 14:
                return f"{numero[:4]}-{numero[4:10]}-{numero[10:]}"
        else:
            # Outros cartões: XXXX-XXXX-XXXX-XXXX
            if len(numero) == 16:
                return f"{numero[:4]}-{numero[4:8]}-{numero[8:12]}-{numero[12:]}"

        # Formatação padrão se não couber em nenhuma categoria
        return numero


def main():
    """
    Função principal para demonstrar o uso do validador.
    """
    validador = ValidadorCartaoCredito()

    print("=" * 70)
    print("VALIDADOR DE BANDEIRAS DE CARTÃO DE CRÉDITO")
    print("=" * 70)
    print()

    # Números de exemplo para teste
    numeros_teste = [
        '4111111111111111',      # Visa válido
        '5555555555554444',      # Mastercard válido
        '378282246310005',       # American Express válido
        '6362970000457013',      # Elo válido
        '6062825624254001',      # Hipercard válido
        '30569309025904',        # Diners Club válido
        '6011111111111117',      # Discover válido
        '4111 1111 1111 1112',   # Visa inválido (dígito verificador errado)
        '1234567890123456',      # Número inválido
        '123',                   # Muito curto
    ]

    print("EXEMPLOS DE VALIDAÇÃO:")
    print()

    for i, numero in enumerate(numeros_teste, 1):
        resultado = validador.validar_cartao(numero)

        print(f"{i:2d}. Número: {numero}")
        if resultado['valido_completo']:
            numero_formatado = validador.formatar_numero(resultado['numero_limpo'], resultado['bandeira'])
            print(f"    Formatado: {numero_formatado}")
        print(f"    Bandeira: {resultado['bandeira'] or 'Não identificada'}")
        print(f"    Comprimento: {resultado['comprimento']} dígitos")
        print(f"    Luhn: {'✓' if resultado['valido_luhn'] else '✗'}")
        print(f"    Status: {resultado['mensagem']}")
        print()

    # Demonstrar uso interativo
    print("=" * 70)
    print("MODO INTERATIVO")
    print("=" * 70)
    print("Digite números de cartão para validar (ou 'sair' para terminar):")
    print()

    while True:
        try:
            entrada = input("Digite o número do cartão: ").strip()

            if entrada.lower() in ['sair', 'quit', 'exit', '']:
                break

            resultado = validador.validar_cartao(entrada)

            print(f"\nResultado:")
            print(f"  Número original: {resultado['numero_original']}")
            print(f"  Número limpo: {resultado['numero_limpo']}")
            if resultado['valido_completo']:
                numero_formatado = validador.formatar_numero(resultado['numero_limpo'], resultado['bandeira'])
                print(f"  Número formatado: {numero_formatado}")
            print(f"  Bandeira: {resultado['bandeira'] or 'Não identificada'}")
            print(f"  Válido (Luhn): {'Sim' if resultado['valido_luhn'] else 'Não'}")
            print(f"  Completamente válido: {'Sim' if resultado['valido_completo'] else 'Não'}")
            print(f"  Status: {resultado['mensagem']}")
            print()

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Erro: {e}")
            print()

    print("\nObrigado por usar o Validador de Cartão de Crédito!")


if __name__ == "__main__":
    main()
