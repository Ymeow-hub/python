from flask import Flask, request
from html import escape
import csv
from typing import List, Dict, Optional, Tuple, Any

app = Flask(__name__)

students: Dict[int, Dict[str, str]] = {}
hw1: Dict[int, int] = {}
hw2: Dict[int, int] = {}
next_id: int = 1

def read_csv(filepath: str) -> List[Dict[str, Any]]:
    result = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if len(row) >= 4:
                    name = row[0].strip()
                    group = row[1].strip()
                    score_str = row[3].strip()
                    score = int(score_str) if score_str.isdigit() else 0
                    if name:
                        result.append({'name': name, 'group': group, 'score': score})
    except FileNotFoundError:
        print(f"Файл {filepath} не найден!")
    return result

def add_student(name: str, group: str, hw_name: str, score: int) -> None:
    global next_id
    found_id = None
    for sid, info in students.items():
        if info['name'] == name and info['group'] == group:
            found_id = sid
            break
    
    if found_id is None:
        student_id = next_id
        next_id += 1
        students[student_id] = {'name': name, 'group': group}
    else:
        student_id = found_id
    
    if hw_name == 'hw-01':
        hw1[student_id] = score
    elif hw_name == 'hw-02':
        hw2[student_id] = score

def load_data() -> None:
    for row in read_csv('python-2025 - big-hw-01.csv'):
        add_student(row['name'], row['group'], 'hw-01', row['score'])
    for row in read_csv('python-2025 - big-hw-02.csv'):
        add_student(row['name'], row['group'], 'hw-02', row['score'])

def average(scores: List[int]) -> Optional[float]:
    return round(sum(scores) / len(scores), 2) if scores else None

def get_mark(score: int) -> int:
    if score >= 50: return 5
    if score >= 30: return 4
    if score >= 1: return 3
    return 2

def get_scores(hw_name: str, group: Optional[str] = None) -> List[int]:
    scores_dict = hw1 if hw_name == 'hw-01' else hw2
    result = []
    for sid, score in scores_dict.items():
        if group is None or students[sid]['group'] == str(group):
            result.append(score)
    return result

@app.route('/names')
def names() -> Dict[str, List[str]]:
    return {'names': [info['name'] for info in students.values()]}

@app.route('/<hw_name>/mean_score')
def hw_mean(hw_name: str):
    if hw_name not in ['hw-01', 'hw-02']:
        return {'error': 'unknown'}, 400
    avg = average(get_scores(hw_name))
    return {'mean_score': avg} if avg else ({'error': 'empty'}, 404)

@app.route('/<hw_name>/<group_id>/mean_score')
def group_mean(hw_name: str, group_id: str):
    if hw_name not in ['hw-01', 'hw-02']:
        return {'error': 'unknown'}, 400
    scores = get_scores(hw_name, group=group_id)
    avg = average(scores)
    return {'mean_score': avg} if avg else ({'error': 'not found'}, 404)

@app.route('/mean_score')
def mean_args():
    hw_name = request.args.get('hw_name')
    group_id = request.args.get('group_id')
    if not hw_name or not group_id:
        return {'error': 'need params'}, 400
    if hw_name not in ['hw-01', 'hw-02']:
        return {'error': 'unknown'}, 400
    scores = get_scores(hw_name, group=group_id)
    avg = average(scores)
    return {'mean_score': avg} if avg else ({'error': 'not found'}, 404)

@app.route('/mark')
def mark_endpoint():
    student_id = request.args.get('student_id')
    group_id = request.args.get('group_id')
    
    if student_id:
        sid = int(student_id)
        if sid not in students:
            return {'error': 'not found'}, 404
        total = hw1.get(sid, 0) + hw2.get(sid, 0)
        return {'student_id': sid, 'mark': get_mark(total), 'total': total}
    
    if group_id:
        marks = []
        for sid, info in students.items():
            if info['group'] == str(group_id):
                total = hw1.get(sid, 0) + hw2.get(sid, 0)
                marks.append(get_mark(total))
        return {'group_id': group_id, 'mean_mark': average(marks)} if marks else ({'error': 'not found'}, 404)
    
    return {'error': 'need id'}, 400

@app.route('/var/k')
def var_k():
    student_id = request.args.get('student_id')
    group_id = request.args.get('group_id')
    
    if student_id:
        sid = int(student_id)
        if sid not in students:
            return {'error': 'not found'}, 404
        total = hw1.get(sid, 0) + hw2.get(sid, 0)
        return {'student_id': sid, 'mark': get_mark(total), 'total': total}
    
    if group_id:
        marks = []
        for sid, info in students.items():
            if info['group'] == str(group_id):
                total = hw1.get(sid, 0) + hw2.get(sid, 0)
                marks.append(get_mark(total))
        return {'group_id': group_id, 'mean_mark': average(marks)} if marks else ({'error': 'not found'}, 404)
    
    return {'error': 'need id'}, 400

@app.route('/course_table')
def table():
    hw_name = request.args.get('hw_name')
    group_id = request.args.get('group_id')
    
    if not hw_name or hw_name not in ['hw-01', 'hw-02']:
        return {'error': 'need hw_name'}, 400
    
    scores_dict = hw1 if hw_name == 'hw-01' else hw2
    
    html = '<table border="1">'
    html += '<tr><th>ID</th><th>Имя</th><th>Группа</th><th>Баллы</th></tr>'
    count = 0
    for sid in sorted(students.keys()):
        if group_id and students[sid]['group'] != str(group_id):
            continue
        html += f'<tr><td>{sid}</td><td>{escape(students[sid]["name"])}</td>'
        html += f'<td>{escape(students[sid]["group"])}</td><td>{scores_dict.get(sid, 0)}</td></tr>'
        count += 1
    
    html += '<table>'
    return html if count > 0 else ({'error': 'empty'}, 404)

if __name__ == '__main__':
    load_data()
    app.run(host='127.0.0.1', port=1337, debug=True)