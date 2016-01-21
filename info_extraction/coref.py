import os
from nltk.tree import Tree
from i2b2.mallet import Instance

def get_ready_for_parsing(input_path):
    input_path = os.path.abspath(input_path)
    dirname, basename = os.path.split(input_path)
    output_base_pieces = basename.split('.')[:-2]
    output_base_pieces.append('tbp')
    output_base = '.'.join(output_base_pieces)
    output_path = os.path.join(dirname, output_base)
    with open(input_path, 'r') as in_fp:
        with open(output_path, 'w') as out_fp:
            for line in in_fp:
                line = line.strip()
                if line == '':
                    continue
                sent = []
                for t in line.split():
                    token = t.split('_')[0]
                    sent.append(token)
                sent.insert(0, '<s>')
                sent.append('</s>')
                out_fp.write(' '.join(sent) + '\n\n')

def call_charniak_parser(tbp_path):
    tbp_path = os.path.abspath(tbp_path)
    dirname, basename = os.path.split(tbp_path)
    output_base_pieces = basename.split('.')[:-1]
    output_base_pieces.append('parsed')
    output_base = '.'.join(output_base_pieces)
    output_path = os.path.join(dirname, output_base)
    cmd = '/home/j/clp/chinese/bin/charniak-parse.sh %(tbp)s 1> %(parsed)s' % {'tbp': tbp_path, 'parsed': output_path}
    os.system(cmd)

def load_parse_doc(parse_path):
    parse_path = os.path.abspath(parse_path)
    parses = []
    with open(parse_path, 'r') as fp:
        for line in fp:
            line = line.strip()
            if line == '':
                continue
            parse = Tree.parse(line)
            parses.append(parse)
    return parses

class Sentence(object):
    """docstring for Sentence"""

    def __init__(self, parse=None):
        super(Sentence, self).__init__()
        self.parse = parse
        self.ms = []

    def insert(self, e):
        start_indices = [m.span[0] for m in self.ms]
        for i in range(len(start_indices)):
            if e.span[0] < start_indices[i]:
                self.ms.insert(i, e)
                return i
        self.ms.append(e)
        return len(self.ms) - 1

class Mention(object):
    """docstring for Mention"""

    def __init__(self):
        super(Mention, self).__init__()
        self.span = None
        self.form = None
        self.type = None

class Pair(object):
    """docstring for Pair"""

    def __init__(self):
        super(Pair, self).__init__()
        self.doc_id = None
        self.m1_sent_num = None
        self.m1_sent = None
        self.m1 = None
        self.m2_sent_num = None
        self.m2_sent = None
        self.m2 = None
        self.label = None
        
def load_pair(input_path, doc_folder):
    input_path = os.path.abspath(input_path)
    ms = {}
    pairs = []
    current_doc_id = None
    current_doc = None
    with open(input_path, 'r') as in_fp:
        for line in in_fp:
            attrs = line.strip().split()
            p = Pair()
            p.doc_id = attrs[0]
            m1_id = '_'.join([p.doc_id, attrs[1], attrs[2], attrs[3]])
            if m1_id not in ms:
                ms[m1_id] = Mention()
            p.m1 = ms[m1_id]
            p.m1_sent_num = int(attrs[1])
            p.m1.span = (int(attrs[2]), int(attrs[3]))
            p.m1.type = attrs[4]
            p.m1.form = attrs[5]
            m2_id = '_'.join([p.doc_id, attrs[6], attrs[7], attrs[8]])
            if m2_id not in ms:
                ms[m2_id] = Mention()
            p.m2 = ms[m2_id]
            p.m2_sent_num = int(attrs[6])
            p.m2.span = (int(attrs[7]), int(attrs[8]))
            p.m2.type = attrs[9]
            p.m2.form = attrs[10]
            try:
                p.label = attrs[11]
            except IndexError:
                pass
            if p.doc_id != current_doc_id:
                current_doc_id = p.doc_id
                current_doc = load_parse_doc(doc_folder + '/' + p.doc_id + '.parsed')
            #try:
            p.m1_sent = Sentence(current_doc[p.m1_sent_num])
            #    p.m1_sent.parse.pos()[p.m1.span[1] - 1]
            #except IndexError:
            #    continue
            try:
                p.m1_sent.ms.index(p.m1)
            except ValueError:
                p.m1_sent.insert(p.m1)
            #try:
            p.m2_sent = Sentence(current_doc[p.m2_sent_num])
            #    p.m2_sent.parse.pos()[p.m2.span[1] - 1]
            #except IndexError:
            #    continue
            try:
                p.m2_sent.ms.index(p.m2)
            except ValueError:
                p.m2_sent.insert(p.m2)
            pairs.append(p)
    return pairs

def generate_feature_file(pairs, feats, output_path):
    with open(output_path, 'w') as fp:
        id_ = 0
        for pair in pairs:
            inst = Instance(str(id_))
            if pair.label:
                inst.label = pair.label
            for f in feats:
                fv = f(pair)
                if fv:
                    feat = '='.join([f.func_name, fv]) 
                    inst.add_feat(feat)
            #fp.write(str(inst) + '\n')
            fp.write(inst.to_str() + '\n')
            id_ += 1





