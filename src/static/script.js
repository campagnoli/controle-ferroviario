// Configuração da API
const API_BASE = '/api';

// Variáveis globais
let chart = null;
let trensData = [];
let infoTurno = {};

// Inicialização da aplicação
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    loadData();
});

// Inicializa a aplicação
function initializeApp() {
    // Define a data atual
    const hoje = new Date().toISOString().split('T')[0];
    document.getElementById('dia').value = hoje;
    
    // Inicializa o gráfico
    initializeChart();
}

// Configura os event listeners
function setupEventListeners() {
    // Informações do turno
    document.getElementById('agente').addEventListener('change', saveInfoTurno);
    document.getElementById('dia').addEventListener('change', saveInfoTurno);
    document.getElementById('feriado').addEventListener('change', saveInfoTurno);
    document.getElementById('turno').addEventListener('change', saveInfoTurno);
    
    // Botões da tabela
    document.getElementById('btn-adicionar-trem').addEventListener('click', adicionarTrem);
    document.getElementById('btn-limpar-dados').addEventListener('click', limparDados);
    
    // Botões de exportação
    document.getElementById('btn-gerar-pdf').addEventListener('click', gerarPDF);
    document.getElementById('btn-gerar-imagem').addEventListener('click', gerarImagem);
    document.getElementById('btn-salvar-dados').addEventListener('click', salvarDados);
}

// Carrega dados do servidor
async function loadData() {
    try {
        // Carrega informações do turno
        const infoResponse = await fetch(`${API_BASE}/info-turno`);
        if (infoResponse.ok) {
            infoTurno = await infoResponse.json();
            updateInfoTurnoForm();
        }
        
        // Carrega dados dos trens
        const trensResponse = await fetch(`${API_BASE}/trens`);
        if (trensResponse.ok) {
            trensData = await trensResponse.json();
            renderTabelaTrens();
            updateEstatisticas();
        }
    } catch (error) {
        console.error('Erro ao carregar dados:', error);
    }
}

// Atualiza o formulário de informações do turno
function updateInfoTurnoForm() {
    document.getElementById('agente').value = infoTurno.agente || '';
    document.getElementById('dia').value = infoTurno.dia || '';
    document.getElementById('feriado').value = infoTurno.feriado || 'Não';
    document.getElementById('turno').value = infoTurno.turno || 'Dia';
}

// Salva informações do turno
async function saveInfoTurno() {
    infoTurno = {
        agente: document.getElementById('agente').value,
        dia: document.getElementById('dia').value,
        feriado: document.getElementById('feriado').value,
        turno: document.getElementById('turno').value
    };
    
    try {
        await fetch(`${API_BASE}/info-turno`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(infoTurno)
        });
    } catch (error) {
        console.error('Erro ao salvar informações do turno:', error);
    }
}

// Renderiza a tabela de trens
function renderTabelaTrens() {
    const tbody = document.getElementById('tbody-trens');
    tbody.innerHTML = '';
    
    trensData.forEach((trem, index) => {
        const row = createTremRow(trem, index);
        tbody.appendChild(row);
    });
}

// Cria uma linha da tabela de trens
function createTremRow(trem, index) {
    const row = document.createElement('tr');
    
    row.innerHTML = `
        <td>${index + 1}</td>
        <td><input type="text" value="${trem.trem || ''}" onchange="updateTrem(${index}, 'trem', this.value)"></td>
        <td><input type="text" value="${trem.origem || ''}" onchange="updateTrem(${index}, 'origem', this.value)"></td>
        <td><input type="time" value="${trem.partida_programada || ''}" onchange="updateTrem(${index}, 'partida_programada', this.value)"></td>
        <td><input type="text" value="${trem.destino || ''}" onchange="updateTrem(${index}, 'destino', this.value)"></td>
        <td><input type="time" value="${trem.chegada_programada || ''}" onchange="updateTrem(${index}, 'chegada_programada', this.value)"></td>
        <td><input type="time" value="${trem.partida_real || ''}" onchange="updateTremComStatus(${index}, 'partida_real', this.value)"></td>
        <td class="status-${trem.status_partida || 'para-circular'}">${getStatusText(trem.status_partida)}</td>
        <td><input type="time" value="${trem.chegada_real || ''}" onchange="updateTremComStatus(${index}, 'chegada_real', this.value)"></td>
        <td class="status-${trem.status_chegada || 'para-circular'}">${getStatusText(trem.status_chegada)}</td>
        <td><textarea onchange="updateTrem(${index}, 'observacoes', this.value)">${trem.observacoes || ''}</textarea></td>
        <td><button class="btn btn-danger" onclick="removerTrem(${index})">Remover</button></td>
    `;
    
    return row;
}

// Atualiza um campo do trem
function updateTrem(index, field, value) {
    if (trensData[index]) {
        trensData[index][field] = value;
        saveTrensData();
    }
}

// Atualiza um campo do trem e recalcula status
async function updateTremComStatus(index, field, value) {
    if (trensData[index]) {
        trensData[index][field] = value;
        
        // Recalcula status
        try {
            const response = await fetch(`${API_BASE}/calcular-status`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(trensData[index])
            });
            
            if (response.ok) {
                const tremAtualizado = await response.json();
                trensData[index] = tremAtualizado;
                renderTabelaTrens();
                updateEstatisticas();
            }
        } catch (error) {
            console.error('Erro ao calcular status:', error);
        }
        
        saveTrensData();
    }
}

// Salva dados dos trens
async function saveTrensData() {
    try {
        await fetch(`${API_BASE}/trens`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(trensData)
        });
        updateEstatisticas();
    } catch (error) {
        console.error('Erro ao salvar dados dos trens:', error);
    }
}

// Adiciona um novo trem
async function adicionarTrem() {
    try {
        const response = await fetch(`${API_BASE}/trens/adicionar`, {
            method: 'POST'
        });
        
        if (response.ok) {
            await loadData();
        }
    } catch (error) {
        console.error('Erro ao adicionar trem:', error);
    }
}

// Remove um trem
async function removerTrem(index) {
    if (confirm('Tem certeza que deseja remover este trem?')) {
        try {
            const response = await fetch(`${API_BASE}/trens/${index}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                await loadData();
            }
        } catch (error) {
            console.error('Erro ao remover trem:', error);
        }
    }
}

// Limpa todos os dados
async function limparDados() {
    if (confirm('Tem certeza que deseja limpar todos os dados? Esta ação não pode ser desfeita.')) {
        try {
            const response = await fetch(`${API_BASE}/limpar-dados`, {
                method: 'POST'
            });
            
            if (response.ok) {
                await loadData();
            }
        } catch (error) {
            console.error('Erro ao limpar dados:', error);
        }
    }
}

// Atualiza estatísticas e gráfico
async function updateEstatisticas() {
    try {
        const response = await fetch(`${API_BASE}/estatisticas`);
        if (response.ok) {
            const stats = await response.json();
            
            // Atualiza números
            document.getElementById('stat-atrasado').textContent = stats.atrasado;
            document.getElementById('stat-ontime').textContent = stats.ontime;
            document.getElementById('stat-para-circular').textContent = stats.para_circular;
            document.getElementById('stat-circulando').textContent = stats.circulando;
            document.getElementById('stat-extra').textContent = stats.extra;
            
            // Atualiza gráfico
            updateChart(stats);
        }
    } catch (error) {
        console.error('Erro ao atualizar estatísticas:', error);
    }
}

// Inicializa o gráfico
function initializeChart() {
    const ctx = document.getElementById('grafico-status').getContext('2d');
    
    chart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Atrasado', 'OnTime', 'Para Circular', 'Circulando', 'Extra'],
            datasets: [{
                data: [0, 0, 0, 0, 0],
                backgroundColor: [
                    '#e74c3c',  // Atrasado
                    '#2ecc71',  // OnTime
                    '#f39c12',  // Para Circular
                    '#3498db',  // Circulando
                    '#95a5a6'   // Extra
                ],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// Atualiza o gráfico
function updateChart(stats) {
    if (chart) {
        chart.data.datasets[0].data = [
            stats.atrasado,
            stats.ontime,
            stats.para_circular,
            stats.circulando,
            stats.extra
        ];
        chart.update();
    }
}

// Converte status para texto
function getStatusText(status) {
    const statusMap = {
        'ontime': 'OnTime',
        'atrasado': 'Atrasado',
        'para_circular': 'Para Circular',
        'circulando': 'Circulando',
        'extra': 'Extra'
    };
    return statusMap[status] || 'Para Circular';
}

// Mostra/esconde loading
function showLoading() {
    document.getElementById('loading-overlay').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loading-overlay').style.display = 'none';
}

// Gera PDF
async function gerarPDF() {
    showLoading();
    try {
        const response = await fetch(`${API_BASE}/gerar-pdf`, {
            method: 'POST'
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `relatorio_trens_${new Date().toISOString().slice(0, 10)}.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } else {
            alert('Erro ao gerar PDF');
        }
    } catch (error) {
        console.error('Erro ao gerar PDF:', error);
        alert('Erro ao gerar PDF');
    } finally {
        hideLoading();
    }
}

// Gera imagem
async function gerarImagem() {
    showLoading();
    try {
        const response = await fetch(`${API_BASE}/gerar-imagem`, {
            method: 'POST'
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `resumo_trens_${new Date().toISOString().slice(0, 10)}.png`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } else {
            alert('Erro ao gerar imagem');
        }
    } catch (error) {
        console.error('Erro ao gerar imagem:', error);
        alert('Erro ao gerar imagem');
    } finally {
        hideLoading();
    }
}

// Salva dados (força salvamento)
async function salvarDados() {
    showLoading();
    try {
        await saveInfoTurno();
        await saveTrensData();
        alert('Dados salvos com sucesso!');
    } catch (error) {
        console.error('Erro ao salvar dados:', error);
        alert('Erro ao salvar dados');
    } finally {
        hideLoading();
    }
}

