# coding=utf-8
from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import ch
ch.set_ch()  # 设置unicode编码中文显示，ch.py位于Lib文件夹

class PPG_handle(FigureCanvas):

    def __init__(self,x_list,y_list, parent=None):
        self.x=x_list
        self.y=y_list
        self.fig = Figure()
        self.fig.suptitle(u"电量描点绘图", fontsize=14).set_color("g")
        self.axes = self.fig.add_subplot(111)
        self.axes.set_autoscale_on(False)
        self.axes.set_xlabel(u"时间(30min)", fontsize=14).set_color("g")
        self.axes.set_ylabel(u"电量百分比", fontsize=14).set_color("g")
        self.axes.grid(False)
        self.compute_initial_figure(self.x,self.y)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class MyStaticMplCanvas(PPG_handle):
    def compute_initial_figure(self,y_list,x_list):
        x=x_list
        percent=y_list
        # print(x_list)
        # print(y_list)
        self.axes.set_xticks(range(1, x_list[-1]+2, 5))
        self.axes.set_yticks(range(0, 105,5))
        #self.axes.set_yticks(range(0, 4300, 100))
            
        self.XLD, = self.axes.plot(x, percent, "b",label="电量")
        self.axes.legend()


def read_vol():
    x_list=[]
    y_list=[]
    j=0
    try:
        with open("./result/system_log.txt","r",encoding="utf-8") as fp:
            lines=fp.readlines()
        for line in lines:
            if "电量" in line:
                percent=line.split("电量:")[1].split("%,")[0]
                y_list.append(int(percent))
                x_list.append(j)
                j+=30
            # if "电压" in line:
            #     vol=line.split("电压:")[1].split("'")[0]
            #     y_list.append(int(vol))
            #     x_list.append(j)
            #     j+=30

        return y_list,x_list
    except Exception as e:
        pass

    
if __name__ == '__main__':
     x_list,y_list,=read_vol()
     sc = MyStaticMplCanvas(x_list,y_list)
     sc.show()
     sc.print_figure('vol_percent.png')

