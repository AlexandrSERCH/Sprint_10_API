## Установка

### 1. Клонировать репозиторий

```bash
git clone <url>
cd <project-folder>
```

### 2. Создать виртуальное окружение

```bash
py -3.12 -m venv .venv
```

### 3. Активировать

**Git Bash / Mac / Linux:**

```bash
source .venv/Scripts/activate
```

**Windows CMD:**

```cmd
.venv\Scripts\activate.bat
```

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

После активации в начале строки появится `(.venv)`.

### 4. Установить зависимости

```bash
pip install .
```