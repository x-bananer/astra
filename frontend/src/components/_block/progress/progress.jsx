import "./progress.css";

const Progress = ({ title='', value = 0, max = 100, color = '', hint = '' }) => {
    const percent = Math.min(100, Math.max(0, (value / max) * 100));

    return (
        <div className="progress">
            <div className="progress__media">
                <div className={`progress__media-aside progress__media-aside--${color}`}>

                </div>
                <div className="progress__media-main">
                    {title}
                </div>
                {hint && (
                    <span className="progress__media-tooltip-wrapper">
                        <span className="progress__media-tooltip">?</span>
                        <span className="progress__media-tooltip-popup">
                            {hint}
                        </span>
                    </span>
                )}
            </div>
            <p className="progress__text">
                ◆ {value} / {max} 
            </p>
            <div className="progress__bar-wrapper">
                <div className="progress__bar-active" style={{ width: `${percent}%` }}></div>
            </div>
        </div>
    );
};

export default Progress;
