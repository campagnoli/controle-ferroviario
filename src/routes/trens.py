from flask import Blueprint, request, jsonify, session
from datetime import datetime
import json

trens_bp = Blueprint('trens', __name__)

# Estrutura de dados padrão para um trem
def criar_trem_vazio():
    return {
        'numero': '',
        'trem': '',
        'origem': '',
        'partida_programada': '',
        'destino': '',
        'chegada_programada': '',
        'partida_real': '',
        'status_partida': 'para_circular',  # para_circular, ontime, atrasado, circulando
        'chegada_real': '',
        'status_chegada': 'para_circular',
        'observacoes': ''
    }

# Estrutura de dados para informações do turno
def criar_info_turno_vazia():
    return {
        'agente': '',
        'dia': datetime.now().strftime('%d/%m/%Y'),
        'feriado': 'Não',
        'turno': 'Dia'
    }

@trens_bp.route('/info-turno', methods=['GET'])
def get_info_turno():
    """Retorna as informações do turno atual"""
    if 'info_turno' not in session:
        session['info_turno'] = criar_info_turno_vazia()
    return jsonify(session['info_turno'])

@trens_bp.route('/info-turno', methods=['POST'])
def update_info_turno():
    """Atualiza as informações do turno"""
    data = request.get_json()
    session['info_turno'] = data
    return jsonify({'success': True})

@trens_bp.route('/trens', methods=['GET'])
def get_trens():
    """Retorna a lista de trens do turno atual"""
    if 'trens' not in session:
        # Inicializa com alguns trens vazios
        session['trens'] = [criar_trem_vazio() for _ in range(5)]
    return jsonify(session['trens'])

@trens_bp.route('/trens', methods=['POST'])
def update_trens():
    """Atualiza a lista completa de trens"""
    data = request.get_json()
    session['trens'] = data
    return jsonify({'success': True})

@trens_bp.route('/trens/<int:index>', methods=['PUT'])
def update_trem(index):
    """Atualiza um trem específico"""
    data = request.get_json()
    if 'trens' not in session:
        session['trens'] = []
    
    # Garante que a lista tenha o tamanho necessário
    while len(session['trens']) <= index:
        session['trens'].append(criar_trem_vazio())
    
    session['trens'][index] = data
    return jsonify({'success': True})

@trens_bp.route('/trens/adicionar', methods=['POST'])
def adicionar_trem():
    """Adiciona um novo trem à lista"""
    if 'trens' not in session:
        session['trens'] = []
    
    session['trens'].append(criar_trem_vazio())
    return jsonify({'success': True, 'index': len(session['trens']) - 1})

@trens_bp.route('/trens/<int:index>', methods=['DELETE'])
def remover_trem(index):
    """Remove um trem da lista"""
    if 'trens' not in session or index >= len(session['trens']):
        return jsonify({'error': 'Trem não encontrado'}), 404
    
    session['trens'].pop(index)
    return jsonify({'success': True})

@trens_bp.route('/estatisticas', methods=['GET'])
def get_estatisticas():
    """Calcula e retorna as estatísticas dos trens"""
    if 'trens' not in session:
        return jsonify({
            'atrasado': 0,
            'ontime': 0,
            'para_circular': 0,
            'circulando': 0,
            'extra': 0
        })
    
    stats = {
        'atrasado': 0,
        'ontime': 0,
        'para_circular': 0,
        'circulando': 0,
        'extra': 0
    }
    
    for trem in session['trens']:
        # Conta baseado no status de partida se não chegou ainda
        if trem.get('chegada_real'):
            status = trem.get('status_chegada', 'para_circular')
        else:
            status = trem.get('status_partida', 'para_circular')
        
        if status in stats:
            stats[status] += 1
        else:
            stats['extra'] += 1
    
    return jsonify(stats)

@trens_bp.route('/calcular-status', methods=['POST'])
def calcular_status():
    """Calcula automaticamente o status baseado nos horários"""
    data = request.get_json()
    
    # Lógica para calcular status de partida
    if data.get('partida_real') and data.get('partida_programada'):
        try:
            real = datetime.strptime(data['partida_real'], '%H:%M')
            programada = datetime.strptime(data['partida_programada'], '%H:%M')
            
            diff_minutes = (real - programada).total_seconds() / 60
            
            if diff_minutes <= 5:  # Tolerância de 5 minutos
                data['status_partida'] = 'ontime'
            else:
                data['status_partida'] = 'atrasado'
        except:
            data['status_partida'] = 'para_circular'
    elif data.get('partida_real'):
        data['status_partida'] = 'circulando'
    else:
        data['status_partida'] = 'para_circular'
    
    # Lógica para calcular status de chegada
    if data.get('chegada_real') and data.get('chegada_programada'):
        try:
            real = datetime.strptime(data['chegada_real'], '%H:%M')
            programada = datetime.strptime(data['chegada_programada'], '%H:%M')
            
            diff_minutes = (real - programada).total_seconds() / 60
            
            if diff_minutes <= 5:  # Tolerância de 5 minutos
                data['status_chegada'] = 'ontime'
            else:
                data['status_chegada'] = 'atrasado'
        except:
            data['status_chegada'] = 'para_circular'
    elif data.get('chegada_real'):
        data['status_chegada'] = 'circulando'
    else:
        data['status_chegada'] = 'para_circular'
    
    return jsonify(data)

@trens_bp.route('/limpar-dados', methods=['POST'])
def limpar_dados():
    """Limpa todos os dados da sessão"""
    session.clear()
    return jsonify({'success': True})

