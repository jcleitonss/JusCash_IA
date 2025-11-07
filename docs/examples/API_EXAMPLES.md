# 💡 Exemplos de API - JUSCASH

Exemplos práticos de uso da API.

---

## ✅ Processo Aprovado

```bash
curl -X POST http://localhost:8000/api/v1/verificar \
  -H "Content-Type: application/json" \
  -d '{
    "numeroProcesso": "0001234-56.2023.4.05.8100",
    "classe": "Cumprimento de Sentença",
    "esfera": "Federal",
    "documentos": [
      {
        "nome": "Certidão de Trânsito em Julgado",
        "texto": "Certifico que transitou em julgado."
      },
      {
        "nome": "Cálculo de Liquidação",
        "texto": "Valor: R$ 67.592,00"
      }
    ],
    "movimentos": [
      {
        "descricao": "Iniciado cumprimento definitivo"
      }
    ]
  }'
```

**Resposta:**
```json
{
  "decision": "approved",
  "rationale": "Processo transitado (POL-1), valor R$ 67.592 informado (POL-2), superior ao mínimo (POL-3).",
  "citacoes": ["POL-1", "POL-2"]
}
```

---

## ❌ Processo Rejeitado (Valor Baixo)

```bash
curl -X POST http://localhost:8000/api/v1/verificar \
  -H "Content-Type: application/json" \
  -d '{
    "numeroProcesso": "0005678-90.2023.5.01.0001",
    "classe": "Cumprimento de Sentença",
    "esfera": "Federal",
    "documentos": [
      {
        "nome": "Cálculo",
        "texto": "Valor: R$ 800,00"
      }
    ]
  }'
```

**Resposta:**
```json
{
  "decision": "rejected",
  "rationale": "Valor R$ 800 inferior ao mínimo de R$ 1.000 (POL-3).",
  "citacoes": ["POL-3"]
}
```

---

## ❌ Processo Rejeitado (Trabalhista)

```bash
curl -X POST http://localhost:8000/api/v1/verificar \
  -H "Content-Type: application/json" \
  -d '{
    "numeroProcesso": "0001234-56.2023.5.01.0001",
    "esfera": "Trabalhista"
  }'
```

**Resposta:**
```json
{
  "decision": "rejected",
  "rationale": "Esfera trabalhista não é aceita (POL-4).",
  "citacoes": ["POL-4"]
}
```

---

## ⚠️ Processo Incompleto

```bash
curl -X POST http://localhost:8000/api/v1/verificar \
  -H "Content-Type: application/json" \
  -d '{
    "numeroProcesso": "0009999-99.2023.4.05.8100",
    "classe": "Cumprimento de Sentença",
    "documentos": []
  }'
```

**Resposta:**
```json
{
  "decision": "incomplete",
  "rationale": "Falta certidão de trânsito em julgado (POL-8).",
  "citacoes": ["POL-8"]
}
```

---

## 🔍 Health Check

```bash
curl http://localhost:8000/health
```

**Resposta:**
```json
{
  "status": "ok",
  "service": "juscrash-api",
  "version": "1.0.0"
}
```

---

## 📊 Swagger UI

**Acesse:** http://localhost:8000/docs

Teste interativamente todos os endpoints!

---

## 🧪 Testar com Arquivo

```bash
# Criar arquivo
cat > processo.json << 'EOF'
{
  "numeroProcesso": "0001234-56.2023.4.05.8100",
  "classe": "Cumprimento de Sentença",
  "esfera": "Federal"
}
EOF

# Enviar
curl -X POST http://localhost:8000/api/v1/verificar \
  -H "Content-Type: application/json" \
  -d @processo.json
```

---

## 📚 Referências

- **API Docs:** http://localhost:8000/docs
- **Políticas:** [../QUICK_REFERENCE.md](../QUICK_REFERENCE.md)
