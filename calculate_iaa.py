
import csv
import sklearn.metrics
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt    

def show_plot(cm, labels):
        ax= plt.subplot()
        sns.heatmap(cm, annot=True, fmt='g', ax=ax);  #annot=True to annotate cells, ftm='g' to disable scientific notation

        # labels, title and ticks
        ax.set_xlabel('Anno2');ax.set_ylabel('Anno1'); 
        ax.set_title('Confusion Matrix'); 
        ax.xaxis.set_ticklabels(labels); ax.yaxis.set_ticklabels(labels);
        plt.show()


def main():
    with open('0-1000_jeroen.csv', encoding='utf8') as first_annotations, open('0-1000_stijn.csv', encoding='utf8') as second_annotations:

        first_annotations_data = csv.reader(first_annotations)
        first_annotations_labels = []
        first_pers = []
        first_diff = []

        for row in first_annotations_data:
            first_annotations_labels.append(row[5])
            first_pers.append(row[11])
            first_diff.append(row[12])
        first_annotations_labels.pop(0)
        first_pers.pop(0)
        first_diff.pop(0)

        second_annotations_data = csv.reader(second_annotations)
        second_annotations_labels = []
        second_pers = []
        second_diff = []
        for row in second_annotations_data:
            second_annotations_labels.append(row[5])
            second_pers.append(row[11])
            second_diff.append(row[12])
        second_annotations_labels.pop(0)
        second_pers.pop(0)
        second_diff.pop(0)

        print("First annotation:")
        print("Total:{}\t Verif:{}\t UnVerif:{}\t NonArg:{}".format(len(first_annotations_labels), first_annotations_labels.count("Verif"), first_annotations_labels.count("UnVerif"), first_annotations_labels.count("NonArg")))
        print("Pers:{}\t NonPers:{}".format(first_pers.count("Pers"), first_pers.count("NonPers")))
        print("Easy:{}\t Difficult:{}".format(first_diff.count("Easy"), first_diff.count("Difficult")))

        print("Second annotation:")
        print("Total:{}\t Verif:{}\t UnVerif:{}\t NonArg:{}".format(len(second_annotations_labels), second_annotations_labels.count("Verif"), second_annotations_labels.count("UnVerif"), second_annotations_labels.count("NonArg")))
        print("Pers:{}\t NonPers:{}".format(second_pers.count("Pers"), second_pers.count("NonPers")))
        print("Easy:{}\t Difficult:{}".format(second_diff.count("Easy"), second_diff.count("Difficult")))

        cm = confusion_matrix(first_annotations_labels, second_annotations_labels)
        cm_pers = confusion_matrix(first_pers, second_pers)
        cm_diff = confusion_matrix(first_diff, second_diff)

        show_plot(cm, ['NonArg','UnVerif', 'Verif'])
        show_plot(cm_pers, ['-','NonPers', 'Pers'])
        show_plot(cm_diff, ['-','Difficult', 'Easy'])

        first_ver_pers = []
        first_ver_diff = []
        second_ver_pers = []
        second_ver_diff = []

        for i in range(len(first_pers)):
            if first_pers[i] != '':
                if second_pers[i] != '':
                    first_ver_pers.append(first_pers[i])
                    first_ver_diff.append(first_diff[i])
                    second_ver_pers.append(second_pers[i])
                    second_ver_diff.append(second_diff[i])


        cohen_kappa = sklearn.metrics.cohen_kappa_score(first_annotations_labels, second_annotations_labels)
        print("Cohen's Kappa Verif/UnVerif/NonArg = ", cohen_kappa)

        cohen_kappa_pers = sklearn.metrics.cohen_kappa_score(first_ver_pers, second_ver_pers)
        print("Cohen's Kappa Pers/NonPers = ", cohen_kappa_pers)

        cohen_kappa_diff = sklearn.metrics.cohen_kappa_score(first_ver_diff, second_ver_diff)
        print("Cohen's Kappa Easy/Difficult = ", cohen_kappa_diff)

if __name__ == "__main__":
    main()
