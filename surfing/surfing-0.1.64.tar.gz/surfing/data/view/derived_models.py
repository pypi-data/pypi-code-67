from sqlalchemy import CHAR, Column, Integer, Index, BOOLEAN, text, TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import DOUBLE, DATE, DATETIME, SMALLINT


class Base():
    _update_time = Column('_update_time', DATETIME, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))  # 更新时间


# make this column at the end of every derived table
Base._update_time._creation_order = 9999
Base = declarative_base(cls=Base)


class IndexVolatility(Base):
    '''指数波动率'''

    __tablename__ = 'index_volatility'

    index_id = Column(CHAR(20), primary_key=True) # 指数ID
    datetime = Column(DATE, primary_key=True) # 日期
    w1_vol = Column(DOUBLE(asdecimal=False)) # 近一周波动率
    m1_vol = Column(DOUBLE(asdecimal=False)) # 近一月波动率
    m3_vol = Column(DOUBLE(asdecimal=False)) # 近三月波动率
    m6_vol = Column(DOUBLE(asdecimal=False)) # 近半年波动率
    y1_vol = Column(DOUBLE(asdecimal=False)) # 近一年波动率
    y3_vol = Column(DOUBLE(asdecimal=False)) # 近三年波动率
    y5_vol = Column(DOUBLE(asdecimal=False)) # 近五年波动率
    y10_vol = Column(DOUBLE(asdecimal=False)) # 近十年波动率
    this_y_vol = Column(DOUBLE(asdecimal=False)) # 今年以来波动率
    this_s_vol = Column(DOUBLE(asdecimal=False)) # 本季度以来波动率
    cumulative_vol = Column(DOUBLE(asdecimal=False)) # 成立至今波动率

    __table_args__ = (
        Index('idx_index_volatility_datetime', 'datetime'),
    )


class IndexReturn(Base):
    '''指数收益率'''

    __tablename__ = 'index_return'

    index_id = Column(CHAR(20), primary_key=True) # 指数ID
    datetime = Column(DATE, primary_key=True) # 日期
    w1_ret = Column(DOUBLE(asdecimal=False)) # 近一周收益率
    m1_ret = Column(DOUBLE(asdecimal=False)) # 近一月收益率
    m3_ret = Column(DOUBLE(asdecimal=False)) # 近三月收益率
    m6_ret = Column(DOUBLE(asdecimal=False)) # 近半年收益率
    y1_ret = Column(DOUBLE(asdecimal=False)) # 近一年收益率
    y3_ret = Column(DOUBLE(asdecimal=False)) # 近三年收益率
    y5_ret = Column(DOUBLE(asdecimal=False)) # 近五年收益率
    y10_ret = Column(DOUBLE(asdecimal=False)) # 近十年收益率
    this_y_ret = Column(DOUBLE(asdecimal=False)) # 今年以来收益率
    this_s_ret = Column(DOUBLE(asdecimal=False)) # 本季度以来收益率
    cumulative_ret = Column(DOUBLE(asdecimal=False)) # 成立至今收益率

    __table_args__ = (
        Index('idx_index_return_datetime', 'datetime'),
    )


class FundAlpha(Base):
    '''基金超额收益'''

    __tablename__ = 'fund_alpha'

    track_err = Column(DOUBLE(asdecimal=False)) # 跟踪误差
    this_y_alpha = Column(DOUBLE(asdecimal=False)) # 今年以来超额收益
    cumulative_alpha = Column(DOUBLE(asdecimal=False)) # 成立以来超额收益
    w1_alpha = Column(DOUBLE(asdecimal=False)) # 近一周收益率
    m1_alpha = Column(DOUBLE(asdecimal=False)) # 近一月超额收益
    m3_alpha = Column(DOUBLE(asdecimal=False)) # 近三月超额收益
    m6_alpha = Column(DOUBLE(asdecimal=False)) # 近半年超额收益
    y1_alpha = Column(DOUBLE(asdecimal=False)) # 近一年超额收益
    y3_alpha = Column(DOUBLE(asdecimal=False)) # 近三年超额收益
    y5_alpha = Column(DOUBLE(asdecimal=False)) # 近五年超额收益
    y10_alpha = Column(DOUBLE(asdecimal=False)) # 近十年超额收益
    fund_id = Column(CHAR(16), primary_key=True) # 基金ID
    datetime = Column(DATE, primary_key=True) # 日期

    __table_args__ = (
        Index('idx_fund_alpha_datetime', 'datetime'),
    )


class IndexValuationLongTerm(Base):
    '''指数估值'''

    __tablename__ = 'index_valuation_long_term'

    index_id = Column(CHAR(20), primary_key=True) #指数ID
    datetime = Column(DATE, primary_key=True) # 日期

    pb_mrq = Column(DOUBLE(asdecimal=False)) # 市净率-MRQ
    pe_ttm = Column(DOUBLE(asdecimal=False)) # 市盈率-MMT
    roe = Column(DOUBLE(asdecimal=False)) # 净资产收益率
    ps_ttm = Column(DOUBLE(asdecimal=False)) # 市销率—MMT
    dy = Column(DOUBLE(asdecimal=False)) # 股息率
    pcf_ttm = Column(DOUBLE(asdecimal=False)) # 市现率-MMT
    peg_ttm = Column(DOUBLE(asdecimal=False)) # 市盈率相对盈利增长比率-MMT
    pe_pct = Column(DOUBLE(asdecimal=False)) # PE百分位(10/5年)
    pb_pct = Column(DOUBLE(asdecimal=False)) # PB百分位(10/5年)
    roe_pct = Column(DOUBLE(asdecimal=False)) # ROE百分位(10/5年)
    pe_pct_30 = Column(DOUBLE(asdecimal=False)) # PE百分位(10/5年) 30 分位
    pe_pct_70 = Column(DOUBLE(asdecimal=False)) # PE百分位(10/5年) 70 分位
    pb_pct_30 = Column(DOUBLE(asdecimal=False)) # PB百分位(10/5年) 30 分位
    pb_pct_70 = Column(DOUBLE(asdecimal=False)) # PB百分位(10/5年) 70 分位
    roe_pct_30 = Column(DOUBLE(asdecimal=False)) # ROE百分位(10/5年) 30 分位
    roe_pct_70 = Column(DOUBLE(asdecimal=False)) # ROE百分位(10/5年) 70 分位
    val_score = Column(DOUBLE(asdecimal=False)) # 估值评分(10/5年)
    eps_ttm = Column(DOUBLE(asdecimal=False)) # 每股收益—MMT
    ps_pct = Column(DOUBLE(asdecimal=False)) # PS百分位(10/5年)
    est_peg = Column(DOUBLE(asdecimal=False)) # 预测peg
    pe_pct_5_3 = Column(DOUBLE(asdecimal=False)) # PE百分位
    pb_pct_5_3 = Column(DOUBLE(asdecimal=False)) # PB百分位
    ps_pct_5_3 = Column(DOUBLE(asdecimal=False)) # PS百分位
    roe_pct_5_3 = Column(DOUBLE(asdecimal=False)) # ROE百分位

    __table_args__ = (
        Index('idx_index_valuation_long_term_datetime', 'datetime'),
    )

class FundIndicator(Base):
    '''基金评价指标'''

    __tablename__ = 'fund_indicator'
    fund_id = Column(CHAR(10), primary_key=True) # 基金ID
    datetime = Column(DATE, primary_key=True) # 日期
    beta = Column(DOUBLE(asdecimal=False)) # 风险指数
    alpha = Column(DOUBLE(asdecimal=False)) # 投资回报
    track_err = Column(DOUBLE(asdecimal=False)) # 跟踪误差
    timespan = Column(DOUBLE(asdecimal=False)) # 历史数据跨度(年)
    fee_rate = Column(DOUBLE(asdecimal=False)) # 费率
    info_ratio = Column(DOUBLE(asdecimal=False)) # 信息比率
    treynor = Column(DOUBLE(asdecimal=False)) # 特雷诺比率
    mdd = Column(DOUBLE(asdecimal=False)) #净值最大回撤
    down_risk = Column(DOUBLE(asdecimal=False)) #下行风险
    ret_over_period = Column(DOUBLE(asdecimal=False)) #区间收益率
    annual_avg_daily_ret = Column(DOUBLE(asdecimal=False)) #年化日均收益
    annual_vol = Column(DOUBLE(asdecimal=False)) #年化波动率
    annual_ret = Column(DOUBLE(asdecimal=False)) #年化收益
    m_square = Column(DOUBLE(asdecimal=False)) #M平方测度 风险调整收益指标
    time_ret = Column(DOUBLE(asdecimal=False)) #择时收益
    var = Column(DOUBLE(asdecimal=False)) #资产在险值
    r_square = Column(DOUBLE(asdecimal=False)) #决定系数R方
    sharpe = Column(DOUBLE(asdecimal=False)) #夏普率
    year_length = Column(DOUBLE(asdecimal=False)) #成立年限
    alpha_bond = Column(DOUBLE(asdecimal=False)) #alpha 债
    beta_bond = Column(DOUBLE(asdecimal=False)) #beta 债
    alpha_hs300 = Column(DOUBLE(asdecimal=False)) #alpha hs300
    beta_hs300 = Column(DOUBLE(asdecimal=False)) #beta hs300

    __table_args__ = (
        Index('idx_fund_indicator_datetime', 'datetime'),
    )


class FundIndicatorWeekly(Base):
    '''基金评价指标'''

    __tablename__ = 'fund_indicator_weekly'
    fund_id = Column(CHAR(10), primary_key=True) # 基金ID
    datetime = Column(DATE, primary_key=True) # 日期
    beta_w = Column(DOUBLE(asdecimal=False)) # 风险指数
    alpha_w = Column(DOUBLE(asdecimal=False)) # 投资回报
    track_err_w = Column(DOUBLE(asdecimal=False)) # 跟踪误差

    __table_args__ = (
        Index('idx_fund_indicator_datetime_weekly', 'datetime'),
    )

class FundIndicatorMonthly(Base):
    '''基金评价指标（月度）'''

    __tablename__ = 'fund_indicator_monthly'

    fund_id = Column(CHAR(10), primary_key=True)  # 基金ID
    datetime = Column(DATE, primary_key=True)  # 日期
    beta_m = Column(DOUBLE(asdecimal=False), nullable=False)  # beta
    sharpe_ratio_m = Column(DOUBLE(asdecimal=False), nullable=False)  # 夏普比率
    treynor_ratio_m = Column(DOUBLE(asdecimal=False), nullable=False)  # 特雷诺比率
    information_ratio_m = Column(DOUBLE(asdecimal=False), nullable=False)  # 信息比率
    jensen_alpha_m = Column(DOUBLE(asdecimal=False), nullable=False)  # 詹森指数
    calmar_ratio_m = Column(DOUBLE(asdecimal=False), nullable=False)  # 卡玛比率

    __table_args__ = (
        Index('idx_fund_indicator_monthly_datetime_monthly', 'datetime'),
    )


class FundIndicatorAnnual(Base):
    '''基金年度指标'''

    __tablename__ = 'fund_indicator_annual'

    fund_id = Column(CHAR(16), primary_key=True)  # 基金ID
    datetime = Column(DATE, primary_key=True)  # 日期
    beta_annual = Column(DOUBLE(asdecimal=False))  # beta
    alpha_annual = Column(DOUBLE(asdecimal=False))  # alpha
    excess_return_annual = Column(DOUBLE(asdecimal=False))  # 超额收益

    __table_args__ = (
        Index('idx_fund_indicator_datetime_annual', 'datetime'),
    )


class FundIndicatorGroup(Base):
    '''基金评价指标'''

    __tablename__ = 'fund_indicator_group'

    fund_id = Column(CHAR(10), primary_key=True)  # 基金ID
    datetime = Column(DATE, primary_key=True)  # 日期
    data_cycle = Column(CHAR(3), primary_key=True)  # 使用多长时间的数据来计算
    scale = Column(DOUBLE(asdecimal=False))  # 规模
    beta = Column(DOUBLE(asdecimal=False))
    alpha = Column(DOUBLE(asdecimal=False))
    track_err = Column(DOUBLE(asdecimal=False))  # 跟踪误差
    info_ratio = Column(DOUBLE(asdecimal=False))  # 信息比率
    info_ratio_hs300 = Column(DOUBLE(asdecimal=False))  # 相对沪深300的信息比率
    treynor = Column(DOUBLE(asdecimal=False))  # 特雷诺比率
    mdd = Column(DOUBLE(asdecimal=False))  # 净值最大回撤
    mdd_len = Column(DOUBLE(asdecimal=False))  # 最大回撤持续时间
    winning_rate = Column(DOUBLE(asdecimal=False))  # 和mmf的相对胜率
    VaR = Column(DOUBLE(asdecimal=False))  # Value at Risk
    CVaR = Column(DOUBLE(asdecimal=False))  # Expected Shortfall
    ins_holds = Column(DOUBLE(asdecimal=False))  # 机构持有者占比
    hold_num = Column(DOUBLE(asdecimal=False))  # 持有人数量
    leverage = Column(DOUBLE(asdecimal=False))  # 杠杆
    ptm = Column(DOUBLE(asdecimal=False))  # 到期期限
    annual_vol = Column(DOUBLE(asdecimal=False))  # 年化波动率
    annual_ret = Column(DOUBLE(asdecimal=False))  # 年化收益
    sharpe = Column(DOUBLE(asdecimal=False))
    calma_ratio = Column(DOUBLE(asdecimal=False))
    stutzer = Column(DOUBLE(asdecimal=False))
    continue_regress_v = Column(DOUBLE(asdecimal=False))  # 业绩持续性回归系数
    continue_regress_t = Column(DOUBLE(asdecimal=False))  # 业绩持续性回归T值
    continue_stats_v = Column(DOUBLE(asdecimal=False))  # 业绩持续性回归计算值
    stock_cl_alpha = Column(DOUBLE(asdecimal=False))  # cl alpha
    stock_cl_alpha_t = Column(DOUBLE(asdecimal=False))  # cl alpha t值
    stock_cl_alpha_p = Column(DOUBLE(asdecimal=False))  # cl alpha p值
    stock_cl_beta = Column(DOUBLE(asdecimal=False))  # cl beta
    stock_cl_beta_t = Column(DOUBLE(asdecimal=False))  # cl beta t值
    stock_cl_beta_p = Column(DOUBLE(asdecimal=False))  # cl beta p值
    stock_tm_alpha = Column(DOUBLE(asdecimal=False))  # tm alpha
    stock_tm_alpha_t = Column(DOUBLE(asdecimal=False))  # tm alpha t值
    stock_tm_alpha_p = Column(DOUBLE(asdecimal=False))  # tm alpha p值
    stock_tm_beta = Column(DOUBLE(asdecimal=False))  # tm beta
    stock_tm_beta_t = Column(DOUBLE(asdecimal=False))  # tm beta t值
    stock_tm_beta_p = Column(DOUBLE(asdecimal=False))  # tm beta p值
    stock_hm_alpha = Column(DOUBLE(asdecimal=False))  # hm alpha
    stock_hm_alpha_t = Column(DOUBLE(asdecimal=False))  # hm alpha t值
    stock_hm_alpha_p = Column(DOUBLE(asdecimal=False))  # hm alpha p值
    stock_hm_beta = Column(DOUBLE(asdecimal=False))  # hm beta
    stock_hm_beta_t = Column(DOUBLE(asdecimal=False))  # hm beta t值
    stock_hm_beta_p = Column(DOUBLE(asdecimal=False))  # hm beta p值
    abnormal_reason = Column(CHAR(60)) # 未计算因子 异常原因
    __table_args__ = (
        Index('idx_fund_indicator_group_datetime_data_cycle', 'datetime', 'data_cycle'),
    )

class FundScoreExtended(Base):
    '''新基金评分v1'''

    __tablename__ = 'fund_score_extended'

    fund_id = Column(CHAR(16), primary_key=True)  # 基金代码
    datetime = Column(DATE, primary_key=True)  # 日期
    data_cycle = Column(CHAR(3), primary_key=True)  # 使用多长时间的数据来计算
    wind_class_1 = Column(CHAR(16))  # Wind基金一级类型
    ret = Column(DOUBLE(asdecimal=False))  # ret
    vol = Column(DOUBLE(asdecimal=False))  # volatility
    sr = Column(DOUBLE(asdecimal=False))  # sharpe ratio
    ir = Column(DOUBLE(asdecimal=False))  # information ratio
    beta = Column(DOUBLE(asdecimal=False))  # beta
    alpha = Column(DOUBLE(asdecimal=False))  # alpha
    treynor_ratio = Column(DOUBLE(asdecimal=False))  # treynor_ratio
    mdd = Column(DOUBLE(asdecimal=False))  # max drawdown
    timing = Column(DOUBLE(asdecimal=False))  # timing
    ret_score = Column(DOUBLE(asdecimal=False))  # score of ret
    vol_score = Column(DOUBLE(asdecimal=False))  # score of volatility
    sr_score = Column(DOUBLE(asdecimal=False))  # score of sharpe ratio
    ir_score = Column(DOUBLE(asdecimal=False))  # score of information ratio
    beta_score = Column(DOUBLE(asdecimal=False))  # score of beta
    alpha_score = Column(DOUBLE(asdecimal=False))  # score of alpha
    treynor_ratio_score = Column(DOUBLE(asdecimal=False))  # score of treynor_ratio
    mdd_score = Column(DOUBLE(asdecimal=False))  # score of max drawdown
    return_score = Column(DOUBLE(asdecimal=False))  # score of return
    robust_score = Column(DOUBLE(asdecimal=False))  # score of robust
    timing_score = Column(DOUBLE(asdecimal=False))  # score of timing
    selection_score = Column(DOUBLE(asdecimal=False))  # score of selection
    allocation_score = Column(DOUBLE(asdecimal=False))  # score of allocation
    interaction_score = Column(DOUBLE(asdecimal=False))  # score of interaction
    return_rank = Column(DOUBLE(asdecimal=False))  # rank of return
    robust_rank = Column(DOUBLE(asdecimal=False))  # rank of robust
    timing_rank = Column(DOUBLE(asdecimal=False))  # rank of timing
    selection_rank = Column(DOUBLE(asdecimal=False))  # rank of selection
    allocation_rank = Column(DOUBLE(asdecimal=False))  # rank of allocation
    interaction_rank = Column(DOUBLE(asdecimal=False))  # rank of interaction
    total_score = Column(DOUBLE(asdecimal=False), nullable=False)  # score of total
    total_rank = Column(DOUBLE(asdecimal=False))  # rank of total

    __table_args__ = (
        Index('idx_fund_score_extended_datetime_data_cycle', 'datetime', 'data_cycle'),
    )

class FundScoreNew(Base):
    '''新基金评分v2'''

    __tablename__ = 'fund_score_new'

    fund_id = Column(CHAR(16), primary_key=True)  # 基金代码
    datetime = Column(DATE, primary_key=True)  # 日期
    data_cycle = Column(CHAR(3), primary_key=True)  # 使用多长时间的数据来计算
    wind_class_1 = Column(CHAR(16))  # Wind基金一级类型
    return_score = Column(DOUBLE(asdecimal=False))  # 被动指数型、被动指数型债券(均为二级分类)基金为跟踪标的能力，其他为收益能力
    robust_score = Column(DOUBLE(asdecimal=False))  # 稳定性能力
    risk_score = Column(DOUBLE(asdecimal=False))  # 抗风险能力
    timing_score = Column(DOUBLE(asdecimal=False))  # 被动指数型、被动指数型债券(均为二级分类)基金和货基(一二级分类相同)为管理规模能力，其他为择时能力
    selection_score = Column(DOUBLE(asdecimal=False))  # 被动指数型、被动指数型债券(均为二级分类)基金和货基(一二级分类相同)为机构观点，其他为选证能力
    team_score = Column(DOUBLE(asdecimal=False))  # 基金公司团队能力
    total_score = Column(DOUBLE(asdecimal=False), nullable=False)  # 总分
    abnormal_reason = Column(CHAR(60)) # 未计算因子 异常原因

    __table_args__ = (
        Index('idx_fund_score_new_data_cycle', 'data_cycle'),
    )

class AssetAllocationInfo(Base):
    '''十档大类资产组合'''

    __tablename__ = 'asset_allocation_info'
    allocation_id = Column(Integer, primary_key=True) # 组合id
    version = Column(Integer, primary_key=True) # 版本号

    hs300 =  Column(DOUBLE(asdecimal=False)) # 沪深300权重
    csi500 =  Column(DOUBLE(asdecimal=False)) # 中证500权重
    gem =  Column(DOUBLE(asdecimal=False)) # 创业板权重
    sp500rmb =  Column(DOUBLE(asdecimal=False)) # 标普500人民币权重
    national_debt = Column(DOUBLE(asdecimal=False)) # 国债权重
    gold =  Column(DOUBLE(asdecimal=False)) # 黄金权重
    credit_debt =  Column(DOUBLE(asdecimal=False)) # 信用债权重
    dax30rmb = Column(DOUBLE(asdecimal=False)) # 德国dax30权重
    real_state = Column(DOUBLE(asdecimal=False)) # 房地产权重 拼错了
    oil = Column(DOUBLE(asdecimal=False)) # 原油权重
    n225rmb = Column(DOUBLE(asdecimal=False)) # 日经225权重
    cash = Column(DOUBLE(asdecimal=False)) # 现金权重
    mdd = Column(DOUBLE(asdecimal=False)) # 最大回撤
    annual_ret = Column(DOUBLE(asdecimal=False)) # 年化收益
    sharpe = Column(DOUBLE(asdecimal=False)) # 夏普率
    recent_y5_ret = Column(DOUBLE(asdecimal=False)) # 最近五年收益
    annual_vol = Column(DOUBLE(asdecimal=False)) # 年化波动率
    mdd_d1 = Column(DATE) # 最大回撤开始时间
    mdd_d2 = Column(DATE) # 最大回撤结束时间
    start_date = Column(DATE) # 回测开始时间
    end_date = Column(DATE) # 回测结束时间

class StyleAnalysisFactorReturn(Base):
    '''风格分析因子收益'''

    __tablename__ = 'style_analysis_factor_return'

    universe_index = Column(CHAR(20), primary_key=True)  # universe, 全市场股票时值为all
    datetime = Column(DATE, primary_key=True)  # 日期
    latest_size = Column(DOUBLE(asdecimal=False))  # 规模
    bp = Column(DOUBLE(asdecimal=False))  # 价值
    short_term_momentum = Column(DOUBLE(asdecimal=False))  # 短期动量
    long_term_momentum = Column(DOUBLE(asdecimal=False))  # 长期动量
    high_low = Column(DOUBLE(asdecimal=False))  # 波动率
    const = Column(DOUBLE(asdecimal=False))  # 常数项

class BarraCNE5FactorReturn(Base):
    '''Barra CNE5因子收益'''

    __tablename__ = 'barra_cne5_factor_return'

    datetime = Column(DATE, primary_key=True)  # 日期
    market = Column(DOUBLE(asdecimal=False))
    leverage = Column(DOUBLE(asdecimal=False))
    cap = Column(DOUBLE(asdecimal=False))
    momentum = Column(DOUBLE(asdecimal=False))
    bp = Column(DOUBLE(asdecimal=False))
    earning = Column(DOUBLE(asdecimal=False))
    liquidity = Column(DOUBLE(asdecimal=False))
    growth = Column(DOUBLE(asdecimal=False))
    vol = Column(DOUBLE(asdecimal=False))

class AllocationDistribution(Base):
    '''有效前沿下各mdd最优策略'''

    __tablename__ = 'allocation_distribution'

    ef_id = Column(CHAR(8), primary_key=True)  # 有效前沿id
    version = Column(Integer, primary_key=True) # 版本号
    annual_ret = Column(DOUBLE(asdecimal=False)) #年化收益
    csi500 = Column(DOUBLE(asdecimal=False)) # 中证500权重
    gem = Column(DOUBLE(asdecimal=False)) #创业板权重
    gold = Column(DOUBLE(asdecimal=False)) #黄金权重
    hs300 = Column(DOUBLE(asdecimal=False)) #沪深300权重
    mdd = Column(DOUBLE(asdecimal=False)) # 最大回撤
    mdd_up_limit = Column(DOUBLE(asdecimal=False)) #最大回测档位上限
    mmf = Column(DOUBLE(asdecimal=False)) # 货币基金权重
    national_debt = Column(DOUBLE(asdecimal=False)) #国债权重
    sp500rmb = Column(DOUBLE(asdecimal=False)) #标普500权重
    cash = Column(DOUBLE(asdecimal=False)) #现金权重

class FundAIC(Base):
    '''基金定投收益收集'''

    __tablename__ = 'fund_aic'

    fund_id = Column(CHAR(20), primary_key=True)  # 基金ID
    datetime = Column(CHAR(20), primary_key=True)  # 时间
    y1_ret = Column(DOUBLE(asdecimal=False))  # 普通定投一年收益
    y3_ret = Column(DOUBLE(asdecimal=False))  # 普通定投三年收益
    y5_ret = Column(DOUBLE(asdecimal=False))  # 普通定投五年收益
    intel_y1_ret = Column(DOUBLE(asdecimal=False))  # 智能定投一年收益
    intel_y3_ret = Column(DOUBLE(asdecimal=False))  # 智能定投三年收益
    intel_y5_ret = Column(DOUBLE(asdecimal=False))  # 智能定投五年收益

class StyleBox(Base):
    '''基金风格九宫格评分'''

    __tablename__ = 'fund_style_box'

    fund_id = Column(CHAR(20), primary_key=True)  # 基金ID
    datetime = Column(DATE, primary_key=True)  # 时间
    x = Column(DOUBLE(asdecimal=False))  # 价值-平衡-成长维度
    y = Column(DOUBLE(asdecimal=False))  # 小盘-中盘-大盘维度

    __table_args__ = (
        Index('idx_fund_style_box_datetime', 'datetime'),
    )

class StyleReg(Base):
    '''Style 因子收益'''

    __tablename__ = 'style_reg_factor_return'

    datetime = Column(DATE, primary_key=True)  # 日期
    large_g= Column(DOUBLE(asdecimal=False))
    large_v = Column(DOUBLE(asdecimal=False))
    mid_g = Column(DOUBLE(asdecimal=False))
    mid_v = Column(DOUBLE(asdecimal=False))
    small_g = Column(DOUBLE(asdecimal=False))
    small_v = Column(DOUBLE(asdecimal=False))

class FundManagerIndex(Base):
    '''基金经理指数'''

    __tablename__ = 'fund_manager_index'

    manager_id = Column(CHAR(16), primary_key=True)  # 基金经理ID
    datetime = Column(DATE, primary_key=True)  # 日期
    fund_type = Column(CHAR(8), primary_key=True)  # 所管理基金类型
    manager_index = Column(DOUBLE(asdecimal=False))  # 基金经理指数

class FundManagerScore(Base):
    '''基金经理评分以及因子'''

    __tablename__ = 'fund_manager_score'

    manager_id = Column(CHAR(16), primary_key=True)  # 基金经理ID
    datetime = Column(DATE, primary_key=True)  # 日期
    fund_type = Column(CHAR(8), primary_key=True)  # 所管理基金类型
    trade_year = Column(DOUBLE(asdecimal=False))
    annualized_ret = Column(DOUBLE(asdecimal=False))
    annualized_vol = Column(DOUBLE(asdecimal=False))
    sharpe = Column(DOUBLE(asdecimal=False))
    mdd = Column(DOUBLE(asdecimal=False))
    alpha = Column(DOUBLE(asdecimal=False))
    beta = Column(DOUBLE(asdecimal=False))
    track_err = Column(DOUBLE(asdecimal=False))
    fund_size = Column(DOUBLE(asdecimal=False))
    model_alpha = Column(DOUBLE(asdecimal=False))
    model_beta = Column(DOUBLE(asdecimal=False))
    now_comp_year = Column(DOUBLE(asdecimal=False)) # 在当前基金公司时间
    year_ret_std =  Column(DOUBLE(asdecimal=False)) # 每年收益波动率
    score = Column(DOUBLE(asdecimal=False))

    __table_args__ = (
        Index('idx_fund_manager_score_datetime', 'datetime'),
    )

class FundManagerInfo(Base):
    '''基金经理信息'''
    __tablename__ = 'manager_info'

    mng_id = Column(CHAR(10), primary_key=True) # 基金经理id
    start_date = Column(DATE, primary_key=True) # 基金经理任职时间
    fund_id = Column(CHAR(10), primary_key=True) # 代码
    mng_name = Column(CHAR(25)) # 基金经理
    gender = Column(CHAR(2)) # 性别
    birth_year = Column(CHAR(4)) # 出生年份
    education = Column(CHAR(4)) # 学历
    nationality = Column(CHAR(10)) # 国籍
    resume = Column(TEXT) # 简历
    end_date = Column(DATE) # 基金经理离职时间


class FundManagerFundRank(Base):
    '''基金经理基金排名'''
    __tablename__ = 'manager_fund_rank'

    mng_id = Column(CHAR(10), primary_key=True) # 基金经理id
    datetime = Column(DATE, primary_key=True) # 时间
    fund_list = Column(TEXT)


class NewShareFundRank(Base):
    """打新基金榜单"""
    __tablename__ = 'fund_rank_new_share'

    fund_id = Column(CHAR(10), primary_key=True)        # 基金ID
    final_score = Column(DOUBLE(asdecimal=False))       # 最终分数


class AbsReturnFundRank(Base):
    """绝对收益基金榜单"""
    __tablename__ = 'fund_rank_abs_return'

    fund_id = Column(CHAR(10), primary_key=True)        # 基金ID
    final_score = Column(DOUBLE(asdecimal=False))       # 最终分数


class ConvertibleBondFundRank(Base):
    """可转债基金榜单"""
    __tablename__ = 'fund_rank_convertible_bonds'

    fund_id = Column(CHAR(10), primary_key=True)        # 基金ID
    final_score = Column(DOUBLE(asdecimal=False))       # 最终分数


class ThirdPartyPortfolioInfo(Base):
    '''组合基本信息表'''

    __tablename__ = 'third_party_portfolio_info'

    po_id = Column(CHAR(16), primary_key=True)  # 组合ID
    po_src = Column(SMALLINT, nullable=False)  # 组合来源 详见constant.SourceType
    po_name = Column(TEXT, nullable=False)  # 组合名称
    po_desc = Column(TEXT)  # 组合描述
    manager_name = Column(TEXT) # 主理人名称
    rich_desc = Column(TEXT)  # 详细描述
    benchmarks = Column(TEXT) # 业绩比较基准
    start_date = Column(DATE, nullable=False)  # 组合开始日期
    risk_level = Column(CHAR(6))  # 风险级别
    can_aip = Column(BOOLEAN)  # 是否可定投


class ThirdPartyPortfolioTrade(Base):
    '''组合调仓记录表'''

    __tablename__ = 'third_party_portfolio_trade'

    po_id = Column(CHAR(16), primary_key=True)  # 组合ID
    datetime = Column(DATE, primary_key=True)  # 日期
    po_src = Column(SMALLINT, nullable=False)  # 组合来源 详见constant.SourceType
    details = Column(TEXT, nullable=False)  # 调仓详情
    comment = Column(TEXT)


class ThirdPartyPortfolioPositionLatest(Base):
    '''组合最新持仓表'''

    __tablename__ = 'third_party_portfolio_position_latest'

    po_id = Column(CHAR(16), primary_key=True)  # 组合ID
    datetime = Column(DATE, primary_key=True)  # 日期
    po_src = Column(SMALLINT, nullable=False)  # 组合来源 详见constant.SourceType
    position = Column(TEXT, nullable=False)  # 持仓

    __table_args__ = (
        Index('idx_third_party_portfolio_position_latest_po_src', 'po_src'),
    )

class ThirdPartyPortfolioIndicator(Base):
    '''组合最新因子表'''

    __tablename__ = 'third_party_portfolio_indicator'

    po_id = Column(CHAR(16), primary_key=True)  # 组合ID
    datetime = Column(DATE, primary_key=True)  # 日期
    po_src = Column(SMALLINT, nullable=False)  # 组合来源 详见constant.SourceType
    nav = Column(DOUBLE(asdecimal=False), nullable=False)  # 净值（累计复权净值计算得出）
    sharpe_ratio = Column(DOUBLE(asdecimal=False))  # 夏普比率
    mdd = Column(DOUBLE(asdecimal=False), nullable=False)  # 最大回撤
    annual_compounded_ret = Column(DOUBLE(asdecimal=False), nullable=False)  # 年化复合收益率
    daily_ret = Column(DOUBLE(asdecimal=False), nullable=False)  # 最近一天收益率
    weekly_ret = Column(DOUBLE(asdecimal=False))  # 最近一周收益率
    monthly_ret = Column(DOUBLE(asdecimal=False))  # 最近一月收益率
    quarterly_ret = Column(DOUBLE(asdecimal=False))  # 最近一季收益率
    half_yearly_ret = Column(DOUBLE(asdecimal=False))  # 最近半年收益率
    yearly_ret = Column(DOUBLE(asdecimal=False))  # 最近一年收益率
    from_setup_ret = Column(DOUBLE(asdecimal=False), nullable=False)  # 成立以来收益率
    vol_by_day = Column(DOUBLE(asdecimal=False))  # 年化日波动率
    vol_by_week = Column(DOUBLE(asdecimal=False))  # 年化周波动率
    vol_by_month = Column(DOUBLE(asdecimal=False))  # 年化月波动率
    annual_ret = Column(DOUBLE(asdecimal=False), nullable=False)  # 年化收益
    mdd_d1 = Column(DATE, nullable=False)  # 回撤区间高点日期
    mdd_d2 = Column(DATE, nullable=False)  # 回撤区间低点日期
    total_commission = Column(DOUBLE(asdecimal=False), nullable=False)  # 总手续费
    rebalance_times = Column(DOUBLE(asdecimal=False), nullable=False)  # 调仓次数

class FundIndicatorIPOConv(Base):
    '''基金评价指标'''

    __tablename__ = 'fund_indicator_ipo_conv'
    fund_id = Column(CHAR(10), primary_key=True) # 基金ID
    datetime = Column(DATE, primary_key=True) # 日期
    beta = Column(DOUBLE(asdecimal=False)) # 风险指数
    alpha = Column(DOUBLE(asdecimal=False)) # 投资回报
    track_err = Column(DOUBLE(asdecimal=False)) # 跟踪误差
    timespan = Column(DOUBLE(asdecimal=False)) # 历史数据跨度(年)
    fee_rate = Column(DOUBLE(asdecimal=False)) # 费率
    info_ratio = Column(DOUBLE(asdecimal=False)) # 信息比率
    treynor = Column(DOUBLE(asdecimal=False)) # 特雷诺比率
    mdd = Column(DOUBLE(asdecimal=False)) #净值最大回撤
    down_risk = Column(DOUBLE(asdecimal=False)) #下行风险
    ret_over_period = Column(DOUBLE(asdecimal=False)) #区间收益率
    annual_avg_daily_ret = Column(DOUBLE(asdecimal=False)) #年化日均收益
    annual_vol = Column(DOUBLE(asdecimal=False)) #年化波动率
    annual_ret = Column(DOUBLE(asdecimal=False)) #年化收益
    m_square = Column(DOUBLE(asdecimal=False)) #M平方测度 风险调整收益指标
    time_ret = Column(DOUBLE(asdecimal=False)) #择时收益
    var = Column(DOUBLE(asdecimal=False)) #资产在险值
    r_square = Column(DOUBLE(asdecimal=False)) #决定系数R方
    sharpe = Column(DOUBLE(asdecimal=False)) #夏普率
    year_length = Column(DOUBLE(asdecimal=False)) #成立年限

    __table_args__ = (
        Index('idx_fund_indicator_ipo_conv_datetime', 'datetime'),
    )

class TopManagerFunds(Base):
    '''基金经理选基'''

    __tablename__ = 'top_manager_funds'
    datetime = Column(DATE, primary_key=True) # 日期
    top_1 = Column(CHAR(10))  # 第一名基金
    top_2 = Column(CHAR(10))  # 第二名基金
    top_3 = Column(CHAR(10))  # 第三名基金
    top_4 = Column(CHAR(10))  # 第四名基金
    top_5 = Column(CHAR(10))  # 第五名基金
    top_6 = Column(CHAR(10))  # 第六名基金
    top_7 = Column(CHAR(10))  # 第七名基金
    top_8 = Column(CHAR(10))  # 第八名基金
    top_9 = Column(CHAR(10))  # 第九名基金
    top_10 = Column(CHAR(10)) # 第十名基金