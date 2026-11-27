import numpy as np
from sklearn.metrics import confusion_matrix, roc_auc_score, average_precision_score, brier_score_loss

def audit(y, probabilities, threshold=.5):
    y, p = np.asarray(y), np.asarray(probabilities, dtype=float)
    if y.ndim != 1 or p.shape != y.shape or not len(y) or not np.isin(y, [0, 1]).all():
        raise ValueError('Labels and probabilities must be aligned binary vectors')
    if not np.isfinite(p).all() or ((p < 0) | (p > 1)).any() or not 0 <= threshold <= 1:
        raise ValueError('Probabilities and threshold must be in [0, 1]')
    tn, fp, fn, tp = confusion_matrix(y, p >= threshold, labels=[0, 1]).ravel()
    return {'n': len(y), 'positive_rate': float(y.mean()), 'tn': int(tn), 'fp': int(fp), 'fn': int(fn), 'tp': int(tp),
            'recall': float(tp / (tp + fn)) if tp + fn else None,
            'precision': float(tp / (tp + fp)) if tp + fp else None,
            'roc_auc': float(roc_auc_score(y, p)) if len(set(y)) == 2 else None,
            'average_precision': float(average_precision_score(y, p)) if y.sum() else None,
            'brier': float(brier_score_loss(y, p))}

def run(data):
    rows = data['samples']
    evidence = audit([r['label'] for r in rows], [r['probability'] for r in rows], data['threshold'])
    findings = []
    if evidence['recall'] is not None and evidence['recall'] < .5:
        findings.append({'evidence': 'overall.recall', 'finding': 'More than half of positives are missed at the supplied threshold.'})
    for field in ['split_definition', 'feature_timing', 'training_data_hash']:
        if not data.get('metadata', {}).get(field):
            findings.append({'evidence': 'metadata.' + field, 'finding': 'Missing evidence; assessment is limited.'})
    slices = {g: audit([r['label'] for r in rows if r['group'] == g], [r['probability'] for r in rows if r['group'] == g], data['threshold']) for g in sorted({r['group'] for r in rows})}
    return {'dataset': data['dataset'], 'overall': evidence, 'slices': slices, 'findings': findings,
            'limitations': ['No release decision', 'Slice differences alone do not establish unfairness or leakage']}
