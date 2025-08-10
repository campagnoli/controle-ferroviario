from flask import Blueprint, request, jsonify, session, send_file
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch
import io
import os
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageDraw, ImageFont
import numpy as np

relatorios_bp = Blueprint('relatorios', __name__)

def get_status_color(status):
    """Retorna a cor correspondente ao status"""
    colors_map = {
        'ontime': colors.green,
        'atrasado': colors.red,
        'para_circular': colors.yellow,
        'circulando': colors.blue,
        'extra': colors.grey
    }
    return colors_map.get(status, colors.grey)

def get_status_text(status):
    """Retorna o texto correspondente ao status"""
    text_map = {
        'ontime': 'OnTime',
        'atrasado': 'Atrasado',
        'para_circular': 'Para Circular',
        'circulando': 'Circulando',
        'extra': 'Extra'
    }
    return text_map.get(status, 'N/A')

@relatorios_bp.route('/gerar-pdf', methods=['POST'])
def gerar_pdf():
    """Gera um relatório em PDF com os dados dos trens"""
    try:
        # Obtém dados da sessão
        info_turno = session.get('info_turno', {})
        trens = session.get('trens', [])
        
        # Cria buffer para o PDF
        buffer = io.BytesIO()
        
        # Configura o documento PDF em paisagem
        doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), 
                              rightMargin=30, leftMargin=30, 
                              topMargin=30, bottomMargin=30)
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=1  # Centralizado
        )
        
        # Conteúdo do PDF
        story = []
        
        # Título
        title = Paragraph("Status de Circulação - 12 horas", title_style)
        story.append(title)
        
        # Informações do turno
        info_data = [
            ['AGENTE:', info_turno.get('agente', ''), 'DIA:', info_turno.get('dia', ''), 
             'FERIADO:', info_turno.get('feriado', ''), 'TURNO:', info_turno.get('turno', '')]
        ]
        
        info_table = Table(info_data, colWidths=[0.8*inch, 1.5*inch, 0.6*inch, 1*inch, 
                                               0.8*inch, 0.8*inch, 0.8*inch, 1*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 20))
        
        # Cabeçalho da tabela de trens
        headers = ['Nº', 'TREM', 'ORIG', 'PART', 'DEST', 'CHEG', 'PART REAL', 
                  'STATUS PARTIDA', 'CHEG REAL', 'STATUS CHEGADA', 'OBSERVAÇÕES']
        
        # Dados dos trens
        table_data = [headers]
        for i, trem in enumerate(trens):
            if any(trem.values()):  # Só inclui se tiver algum dado
                row = [
                    str(i + 1),
                    trem.get('trem', ''),
                    trem.get('origem', ''),
                    trem.get('partida_programada', ''),
                    trem.get('destino', ''),
                    trem.get('chegada_programada', ''),
                    trem.get('partida_real', ''),
                    get_status_text(trem.get('status_partida', '')),
                    trem.get('chegada_real', ''),
                    get_status_text(trem.get('status_chegada', '')),
                    trem.get('observacoes', '')
                ]
                table_data.append(row)
        
        # Cria a tabela
        if len(table_data) > 1:
            table = Table(table_data, colWidths=[0.4*inch, 0.8*inch, 0.6*inch, 0.7*inch,
                                               0.6*inch, 0.7*inch, 0.8*inch, 1*inch,
                                               0.8*inch, 1*inch, 1.5*inch])
            
            # Estilo da tabela
            table_style = [
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]
            
            # Adiciona cores baseadas no status
            for i, trem in enumerate(trens):
                if any(trem.values()):
                    row_idx = i + 1
                    if row_idx < len(table_data):
                        # Status de partida
                        status_partida = trem.get('status_partida', '')
                        if status_partida:
                            table_style.append(('BACKGROUND', (7, row_idx), (7, row_idx), 
                                              get_status_color(status_partida)))
                        
                        # Status de chegada
                        status_chegada = trem.get('status_chegada', '')
                        if status_chegada:
                            table_style.append(('BACKGROUND', (9, row_idx), (9, row_idx), 
                                              get_status_color(status_chegada)))
            
            table.setStyle(TableStyle(table_style))
            story.append(table)
        
        # Constrói o PDF
        doc.build(story)
        
        # Salva o arquivo
        pdf_path = '/tmp/relatorio_trens.pdf'
        with open(pdf_path, 'wb') as f:
            f.write(buffer.getvalue())
        
        buffer.close()
        
        return send_file(pdf_path, as_attachment=True, 
                        download_name=f'relatorio_trens_{datetime.now().strftime("%Y%m%d_%H%M")}.pdf',
                        mimetype='application/pdf')
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@relatorios_bp.route('/gerar-imagem', methods=['POST'])
def gerar_imagem():
    """Gera uma imagem resumo para corpo de e-mail"""
    try:
        # Obtém dados da sessão
        info_turno = session.get('info_turno', {})
        trens = session.get('trens', [])
        
        # Calcula estatísticas
        stats = {
            'atrasado': 0,
            'ontime': 0,
            'para_circular': 0,
            'circulando': 0,
            'extra': 0
        }
        
        for trem in trens:
            if any(trem.values()):
                # Conta baseado no status de partida se não chegou ainda
                if trem.get('chegada_real'):
                    status = trem.get('status_chegada', 'para_circular')
                else:
                    status = trem.get('status_partida', 'para_circular')
                
                if status in stats:
                    stats[status] += 1
                else:
                    stats['extra'] += 1
        
        # Cria a imagem
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
        fig.suptitle(f'Relatório de Circulação - {info_turno.get("dia", "")} - {info_turno.get("turno", "")}', 
                    fontsize=16, fontweight='bold')
        
        # Gráfico de barras
        labels = ['Atrasado', 'OnTime', 'Para Circular', 'Circulando', 'Extra']
        values = [stats['atrasado'], stats['ontime'], stats['para_circular'], 
                 stats['circulando'], stats['extra']]
        colors_list = ['red', 'green', 'yellow', 'blue', 'grey']
        
        bars = ax1.bar(labels, values, color=colors_list)
        ax1.set_title('Status dos Trens')
        ax1.set_ylabel('Quantidade')
        
        # Adiciona valores nas barras
        for bar, value in zip(bars, values):
            if value > 0:
                ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                        str(value), ha='center', va='bottom', fontweight='bold')
        
        # Gráfico de pizza
        non_zero_values = [(label, value, color) for label, value, color in zip(labels, values, colors_list) if value > 0]
        if non_zero_values:
            pie_labels, pie_values, pie_colors = zip(*non_zero_values)
            ax2.pie(pie_values, labels=pie_labels, colors=pie_colors, autopct='%1.1f%%', startangle=90)
            ax2.set_title('Distribuição dos Status')
        
        # Informações do turno
        info_text = f"Agente: {info_turno.get('agente', 'N/A')}\n"
        info_text += f"Data: {info_turno.get('dia', 'N/A')}\n"
        info_text += f"Turno: {info_turno.get('turno', 'N/A')}\n"
        info_text += f"Total de Trens: {sum(values)}"
        
        fig.text(0.02, 0.02, info_text, fontsize=10, verticalalignment='bottom')
        
        plt.tight_layout()
        
        # Salva a imagem
        img_path = '/tmp/resumo_trens.png'
        plt.savefig(img_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return send_file(img_path, as_attachment=True,
                        download_name=f'resumo_trens_{datetime.now().strftime("%Y%m%d_%H%M")}.png',
                        mimetype='image/png')
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

