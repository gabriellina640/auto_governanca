# Cadastro Inteligente Excel

Aplicativo desktop para cadastrar registros em uma planilha Excel sincronizada pelo OneDrive/SharePoint.

## Fluxo

1. O usuário sincroniza a biblioteca/pasta do SharePoint no OneDrive.
2. Abre o aplicativo.
3. Seleciona o arquivo `.xlsx` na primeira vez.
4. O caminho é salvo automaticamente no `config.json` do usuário.
5. Nas próximas aberturas, o app carrega a mesma planilha sozinho.
6. O usuário preenche o formulário lateral.
7. O app adiciona a linha no Excel, salva e cria backup.
8. O OneDrive sincroniza o arquivo alterado com o SharePoint.

## Requisitos para rodar em desenvolvimento

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Gerar EXE localmente

```bash
pyinstaller --noconfirm --clean --windowed --name "CadastroExcel" --add-data "app/ui/styles.qss;app/ui" main.py
```

O executável fica em:

```text
dist/CadastroExcel/CadastroExcel.exe
```

## Gerar EXE no GitHub Actions

Suba este projeto para um repositório GitHub e rode a action **Build Windows EXE**.

O artifact gerado será:

```text
CadastroExcel-windows
```

## Configuração

O app cria um arquivo `config.json` automaticamente em `%APPDATA%\CadastroExcel\config.json`.

Exemplo:

```json
{
  "app_name": "Cadastro Inteligente Excel",
  "excel_path": "",
  "sheet_name": "",
  "auto_columns": {
    "id": "ID",
    "timestamp": "TimestampInclusao",
    "user": "UsuarioInclusao"
  },
  "hidden_form_fields": [
    "ID",
    "TimestampInclusao",
    "UsuarioInclusao"
  ],
  "required_fields": [],
  "backup_enabled": true,
  "backup_folder": "backups"
}
```

## Estrutura esperada do Excel

A primeira linha precisa ter os cabeçalhos. Exemplo:

```text
ID | TimestampInclusao | UsuarioInclusao | Cliente | Produto | Quantidade | Status
```

Os campos automáticos não aparecem no formulário:

- ID
- TimestampInclusao
- UsuarioInclusao

## Observações

- Use `.xlsx`.
- Evite deixar o arquivo aberto no Excel ao salvar pelo app.
- O app cria backups na pasta `backups` ao lado da planilha.
