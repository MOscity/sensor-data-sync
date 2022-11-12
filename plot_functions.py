from lib import register_matplotlib_converters, plt, mdates, FuncFormatter


def my_date_formater(ax, delta):
    """Formats matplotlib axes 
        """
    if delta.days < 3:
        ax.xaxis.set_major_locator(mdates.DayLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%a, %d-%b-%Y'))
        ax.xaxis.set_minor_formatter(mdates.DateFormatter('%H:%M'))
        ax.xaxis.grid(True, which='minor')
        ax.tick_params(axis="x", which="major", pad=15)
        if delta.days < 0.75:
            ax.xaxis.set_minor_locator(mdates.HourLocator())
        if delta.days < 1:
            ax.xaxis.set_minor_locator(
                mdates.HourLocator((0, 3, 6, 9, 12, 15, 18, 21,)))
        else:
            ax.xaxis.set_minor_locator(mdates.HourLocator((0, 6, 12, 18,)))
    elif delta.days < 8:
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        ax.xaxis.set_minor_formatter(mdates.DateFormatter('%a %d'))
        ax.xaxis.grid(True, which='minor')
        ax.tick_params(axis="x", which="major", pad=15)
        ax.xaxis.set_minor_locator(mdates.DayLocator())
        ax.set(xlabel='date')
    else:
        xtick_locator = mdates.AutoDateLocator()
        xtick_formatter = mdates.AutoDateFormatter(xtick_locator)
        xtick_formatter.scaled[30.] = FuncFormatter(my_days_format_function)
        xtick_formatter.scaled[1.] = FuncFormatter(my_days_format_function)
        ax.xaxis.set_major_locator(xtick_locator)
        ax.xaxis.set_major_formatter(xtick_formatter)
        ax.set(xlabel='date')


def my_days_format_function(x, pos=None):
    """Formats matplotlib dates in daytime.
        """
    x = mdates.num2date(x)
    if pos == 0:
        fmt = '%d. %b\n%Y'
    else:
        fmt = '%d.%m '
    label = x.strftime(fmt)
    return label


def createAllanDeviationPlot(y, x=None, yunits='##', title="mySensor", yTitle='eBC'):
    """Creates a plot from y including labels and units. Written by Alejandro Keller.
        """
    plt.style.use('ggplot')
    register_matplotlib_converters()

    # definitions for the axes
    left, width = 0.1, 0.7
    bottom, height = 0.15, 0.75
    spacing = 0.005
    box_width = 1 - (1.5*left + width + spacing)

    rect_scatter = [left, bottom, width, height]
    rect_box = [left + width + spacing, bottom, box_width, height]

    # start with a rectangular Figure
    box = plt.figure("boxplot", figsize=(12, 6))

    ax_scatter = plt.axes(rect_scatter)
    ax_scatter.tick_params(direction='in', top=True, right=True)
    ax_box = plt.axes(rect_box)
    ax_box.tick_params(direction='in', labelleft=False, labelbottom=False)

    # the scatter plot:
    if x == None:
        ax_scatter.plot(y)  # change plot type to scatter to have markers
        tdelta = y.index.max() - y.index.min()
    else:
        ax_scatter.plot(x, y)  # change plot type to scatter to have markers
        tdelta = x.max() - x.min()
    ax_scatter.set(xlabel='date', ylabel=yTitle +
                   ' (' + yunits + ')', title=title)
    my_date_formater(ax_scatter, tdelta)

    # now determine nice limits by hand:
    # binwidth = 0.25
    lim0 = y.min()
    lim1 = y.max()
    if x == None:
        tlim0 = y.index.min()
        tlim1 = y.index.max()
    else:
        tlim0 = x.min()
        tlim1 = x.max()
    extra_space = (lim1 - lim0)/10
    extra_t = (tlim1 - tlim0)/10
    ax_scatter.set_xlim((tlim0-extra_t, tlim1+extra_t))
    ax_scatter.set_ylim((lim0-extra_space, lim1+extra_space))

    meanpointprops = dict(marker='D')
    ax_box.boxplot(y.dropna(), showmeans=True, meanprops=meanpointprops)
    ax_box.set_ylim(ax_scatter.get_ylim())
    mu = y.mean()
    sigma = y.std()
    text = r'$\mu={0:.2f},\ \sigma={1:.3f}$'.format(mu, sigma)
    ax_box.text(1, lim1 + extra_space/2, text,
                horizontalalignment="center", verticalalignment="center")

    plt.show()
    plt.close()
    del (box)


def createSimplePlot(y, x=None, yunits='##', title="mySensor", yTitle='eBC'):
    """Creates a plot from y including labels and units. Written by Alejandro Keller.
        """
    plt.style.use('ggplot')
    register_matplotlib_converters()

    # definitions for the axes
    left, width = 0.1, 0.7
    bottom, height = 0.15, 0.75
    spacing = 0.005
    box_width = 1 - (1.5*left + width + spacing)

    rect_scatter = [left, bottom, width, height]
    rect_box = [left + width + spacing, bottom, box_width, height]

    # start with a rectangular Figure
    box = plt.figure("boxplot", figsize=(12, 6))

    ax_scatter = plt.axes(rect_scatter)
    ax_scatter.tick_params(direction='in', top=True, right=True)
    ax_box = plt.axes(rect_box)
    ax_box.tick_params(direction='in', labelleft=False, labelbottom=False)

    # the scatter plot:
    if x == None:
        ax_scatter.plot(y)  # change plot type to scatter to have markers
        tdelta = y.index.max() - y.index.min()
    else:
        ax_scatter.plot(x, y)  # change plot type to scatter to have markers
        tdelta = x.max() - x.min()
    ax_scatter.set(xlabel='date', ylabel=yTitle +
                   ' (' + yunits + ')', title=title)
    my_date_formater(ax_scatter, tdelta)

    # now determine nice limits by hand:
    # binwidth = 0.25
    lim0 = y.min()
    lim1 = y.max()
    if x == None:
        tlim0 = y.index.min()
        tlim1 = y.index.max()
    else:
        tlim0 = x.min()
        tlim1 = x.max()
    extra_space = (lim1 - lim0)/10
    extra_t = (tlim1 - tlim0)/10
    ax_scatter.set_xlim((tlim0-extra_t, tlim1+extra_t))
    ax_scatter.set_ylim((lim0-extra_space, lim1+extra_space))

    meanpointprops = dict(marker='D')
    ax_box.boxplot(y.dropna(), showmeans=True, meanprops=meanpointprops)
    ax_box.set_ylim(ax_scatter.get_ylim())
    mu = y.mean()
    sigma = y.std()
    text = r'$\mu={0:.2f},\ \sigma={1:.3f}$'.format(mu, sigma)
    ax_box.text(1, lim1 + extra_space/2, text,
                horizontalalignment="center", verticalalignment="center")

    plt.show()
    plt.close()
    del (box)
