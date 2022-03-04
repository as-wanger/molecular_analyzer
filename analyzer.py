import io
import matplotlib.pyplot as plt
from matplotlib import rc


class Control:
    def __init__(self):
        self.aa = {}
        self.pep = {}
        self.matter = {}
        self.output_log = ""
        self.aa_list = []
        self.possible_container = []
        self.total = 0
        self.alter_total = 0
        self.part = {}
        self.counter = {}
        self.buf = 0

    def add_mw(self, kind, mw):
        self.aa[kind] = mw

    def add_matter(self, matter, formula, mw):
        self.matter[matter] = formula
        self.add_mw(formula, mw)

    def enlarge_types(self):
        l = list(self.pep)
        m = list(self.matter.values())
        for i in l:
            for j in m:
                self.pep[i + '-' + j] = self.pep[i] + '-' + j

    def count_mw(self, amino_acid):
        total, alter_t = 0, 0
        for i in amino_acid:
            if "/" in i:
                total += self.aa[i.split('/')[0]]
                alter_t += self.aa[i.split('/')[1]]
            else:
                total += float(self.aa[i])
                alter_t += float(self.aa[i])
        return round(total, 2), round(alter_t, 2)

    def query(self, query_type, query_type2):
        if query_type2 in self.matter.values():
            query_type = "type" + query_type + "-" + query_type2
        elif query_type2 == "":
            query_type = "type" + query_type
        else:
            return 0

        if query_type in self.pep:
            self.aa_list = self.standardization(query_type)
            part = self.get_particle_and_mw(self.aa_list)
            self.total, self.alter_total = self.count_mw(self.aa_list)

            self.output_log = f"This compound is {query_type}\n" \
                   f"It's formula is {self.pep[query_type]}\n" \
                   f"Amino_acid = {self.aa_list}\n" \
                   f"Total = {self.total:.02f}\n" \
                   f"Alter_t = {self.alter_total:.02f}\n" \
                   f"The particle have {part}\n"
            return 1
        elif query_type == "type+":
            return 1
        elif "+-" in query_type:
            return 1
        else:
            return 0

    def standardization(self, query_type):
        amino_acid = self.pep[query_type].split(' ')[1].split('-')
        return amino_acid

    def get_particle_and_mw(self, amino_acid):
        particle = []
        # get the pieces
        for i in range(1, len(amino_acid)):
            head, tail = amino_acid[:i], amino_acid[i:]
            if head not in particle:
                particle.append(head)
            if tail not in particle:
                particle.append(tail)
            for j in range(1, len(amino_acid)):
                temp = amino_acid[i + 1:len(amino_acid) - j]
                if temp not in particle and temp != []:
                    particle.append(temp)
        particle.append(amino_acid)

        # get pieces' mw
        particle_mw = []
        for i in range(len(particle)):
            particle_mw.append(list(self.count_mw(particle[i])))
            particle[i] = '-'.join(particle[i])

        part = dict(zip(particle, particle_mw))
        part = dict(sorted(part.items(), key=lambda x: x[1]))
        return part


    def all_compounds(self):
        for i in self.pep:
            amino_acid = self.standardization(i)
            self.counter[i] = 0
            part = self.get_particle_and_mw(amino_acid)
            self.part = {**self.part, **part}  # expand the dict
            # conclusion
            # part -> {'Val': [99.07, 99.07], 'Leu': [113.08, 113.08] = types
            # self.aa -> {'FA': 198.16, 'Glu': 129.04, 'Leu': 113.08
            # self.pep -> 'type1': 'β-OH FA-Glu-Leu/Ile-Leu-Val-Asp-Leu-Leu/Ile'
            # self.counter -> {'type1': 0, 'type2': 0
        self.part = dict(sorted(self.part.items(), key=lambda x: x[1]))

    def check_the_parts(self, mw, most_nums, first_variation, near_variation, types):
        self.possible_container = []
        if most_nums <= 0:
            return 0
        elif first_variation <= 0:
            return 0
        elif near_variation <= 0:
            return 0
        else:
            trans_l = list(types.items())
            for ele in mw:
                ele = int(ele[0])
                text = []
                for i in range(len(trans_l)):
                    if int(trans_l[0][1][0]) < ele < int(trans_l[len(trans_l) - 1][1][0]):
                        if ele < trans_l[i][1][0]:
                            if ele - trans_l[i - 1][1][0] < first_variation:
                                text.append(f"{trans_l[i - 1][0]}: {trans_l[i - 1][1][0]}")
                                self.possible_container.append(trans_l[i - 1][0])
                                for j in range(1, most_nums):
                                    if abs(trans_l[i - j][1][0] - trans_l[i - j - 1][1][0]) <= near_variation:
                                        text.append(f"{trans_l[i - j - 1][0]}: {trans_l[i - j - 1][1][0]}")
                                        self.possible_container.append(trans_l[i - j - 1][0])
                                    else:
                                        break
                            if trans_l[i][1][0] - ele < first_variation:
                                text.append(f"{trans_l[i][0]}: {trans_l[i][1][0]}")
                                self.possible_container.append(trans_l[i][0])
                                for j in range(1, most_nums):
                                    if abs(trans_l[i + j - 1][1][0] - trans_l[i + j][1][0]) <= near_variation:
                                        text.append(f"{trans_l[i + j][0]}: {trans_l[i + j][1][0]}")
                                        self.possible_container.append(trans_l[i + j][0])
                                    else:
                                        break
                            break
                    else:
                        return 0
                self.output_log += "Molecular {:} is maybe:\n{:}".format(ele, '\n'.join(text))
                self.output_log += '\n' + "=" * 20 + '\n'
            for i in self.possible_container:
                for k, v in self.pep.items():
                    if i in v:
                        self.counter[k] += 1
            self.counter = dict(sorted(self.counter.items(), key=lambda x: x[1], reverse=True))
            return 1

    def draw(self):
        for_draw = self.counter
        for i in list(for_draw):
            if "-" in i:
                l = i.split("-")
                for_draw[l[0][4:] + "-" + l[1][0]] = for_draw.pop(i)
            else:
                for_draw[i[4:]] = for_draw.pop(i)

        picture_list = list(for_draw.items())
        rc('savefig', format='jpg')

        # 取 dict 鍵值 為 xy
        x, y = zip(*picture_list)
        fig, ax = plt.subplots(figsize=(7, 5))
        # 未使用宣告變數，預留後續拓展
        scatter = ax.scatter(x, y)
        ax.set_xlabel("Possible\ncounts", rotation=0)
        ax.set_ylabel("Peptide\ntype", rotation=0)
        ax.xaxis.set_label_coords(-0.05, -.06)
        ax.yaxis.set_label_coords(-.1, -.05)

        threshold = 5
        # 補值至五倍數 (24 -> 25, 31 -> 35)
        plt.ylim(ymax=(divmod(max(y), threshold)[0] + 1) * threshold, ymin=0)
        plt.xticks(rotation=90)
        buf = io.BytesIO()
        plt.savefig(buf)
        buf.seek(0)
        self.buf = buf


def pretreat_mw(mw_listctrldata: dict):
    return dict([mw_listctrldata[k][0], mw_listctrldata[k][1]] for k in mw_listctrldata)


def pretreat_types(types_listctrldata: dict):
    return dict([types_listctrldata[k][0], types_listctrldata[k][2]] for k in types_listctrldata)
