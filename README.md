
# Sistema de Gestão Hoteleira

Sistema de gestão hoteleira em Python, feito para a disciplina de Computação I. Roda inteiramente no terminal e persiste os dados em arquivos `.txt`, sem depender de banco de dados externo.

## Funcionalidades

**Autenticação**
- Cadastro e login de usuários, com duas áreas de trabalho: Administração e Restaurante
- Setup inicial obrigatório de uma conta de administrador master

**Administração**
- Check-in de hóspedes (dados dos hóspedes, número de noites, escolha de suíte)
- Check-out com cálculo automático do valor total (diárias + consumo no restaurante)
- Consulta de reservas ativas
- Troca de hóspede de quarto/suíte, com recálculo de valor
- Estatísticas financeiras mensais e anuais, com gráfico de barras em ASCII
- Gerenciamento de usuários (listar e excluir)
- Gerenciamento de cardápio (adicionar/remover itens)

**Restaurante**
- Consulta ao cardápio (Comidas, Bebidas, Sobremesas)
- Registro de pedidos vinculados a uma reserva ativa

## Conceitos aplicados

- Manipulação de arquivos (leitura e escrita em `.txt`) para persistência de dados
- Estruturas de dados: dicionários aninhados, listas e tuplas
- Tratamento de exceções (`try`/`except`) para validação de entradas
- Modularização em funções, cada uma com responsabilidade única
- Cálculos com datas (`datetime`, `timedelta`) para relatórios por período

## Como executar

```bash
python HotelManager.py
```

Na primeira execução, o sistema pede a criação de uma conta de administrador. Os dados de usuários, reservas e cardápio ficam salvos automaticamente em `usuarios.txt`, `reservas.txt` e `cardapio.txt`.

## Relatório técnico

O relatório técnico do projeto está disponível em [RelatorioTecnicoHotelManager](https://github.com/dneves1/hotel-management-system/blob/main/RelatorioTecnicoHotelManager.pdf)

