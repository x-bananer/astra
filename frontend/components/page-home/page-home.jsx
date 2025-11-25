"use client";

import { useEffect, useState } from "react";
import styles from './page-home.module.css';
import Progress from '../_block/progress/progress';

const PageHome = () => {

    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function load() {
            try {
                const res = await fetch("http://127.0.0.1:5000/analyze", {
                    method: "GET",
                    headers: {
                        "Accept": "application/json"
                    }
                });

                const json = await res.json();
                setData(json.analysis || null);
            } catch (e) {
                console.error("Failed to load:", e);
            } finally {
                setLoading(false);
            }
        }

        load();
    }, []);

    return (
        <div className={styles['page-home']}>
            <div className={styles['page-home__header']}>
                <h1 className={styles['page-home__title']}>Dashboard</h1>
            </div>

            <div className={styles['page-home__content']}>
                {loading && (
                    <div className={styles['page-home__stub']}>
                        Analyzing your team activity...
                        <br></br>
                        This may take a moment.
                    </div>
                )
                }

                {!data && !loading && (
                    <div className={styles['page-home__stub']}>
                        Oops! No data...
                    </div>
                )
                }

                {data && !loading && (
                    <div className={styles['page-home__grid']}>
                        {(data.overall_score ||
                            data.consistency_score ||
                            data.workload_balance_score ||
                            data.pacing_score ||
                            data.task_completion_ratio_score) && (
                                <div className={styles['page-home__grid-item-1']}>
                                    <div className={styles['page-home__card']}>
                                        <h2 className={styles['page-home__card-title']}>Team Metrics</h2>
                                        <div className={styles['page-home__card-row']}>

                                            {data.overall_score && (
                                                <Progress
                                                    title="Overall Score"
                                                    value={data.overall_score.rate}
                                                    max={data.overall_score.max}
                                                    hint={data.overall_evaluation_explanation}
                                                    color="pink"
                                                />
                                            )}

                                            {data.consistency_score && (
                                                <Progress
                                                    title="Consistency"
                                                    value={data.consistency_score.rate}
                                                    max={data.consistency_score.max}
                                                    hint={data.consistency_score_evaluation_explanation}
                                                    color="blue"
                                                />
                                            )}

                                            {data.workload_balance_score && (
                                                <Progress
                                                    title="Workload balance"
                                                    value={data.workload_balance_score.rate}
                                                    max={data.workload_balance_score.max}
                                                    hint={data.workload_balance_score_evaluation_explanation}
                                                    color="yellow"
                                                />
                                            )}

                                            {data.pacing_score && (
                                                <Progress
                                                    title="Pacing"
                                                    value={data.pacing_score.rate}
                                                    max={data.pacing_score.max}
                                                    hint={data.pacing_score_evaluation_explanation}
                                                    color="green"
                                                />
                                            )}

                                            {data.task_completion_ratio_score && (
                                                <Progress
                                                    title="Completion"
                                                    value={data.task_completion_ratio_score.rate}
                                                    max={data.task_completion_ratio_score.max}
                                                    hint={data.task_completion_ratio_evaluation_explanation}
                                                    color="gray"
                                                />
                                            )}

                                            {data.collaboration_density_score && (
                                                <Progress
                                                    title="Collaboration Density"
                                                    value={data.collaboration_density_score.rate}
                                                    max={data.collaboration_density_score.max}
                                                    hint={data.collaboration_density_evaluation_explanation}
                                                    color="purple"
                                                />
                                            )}
                                        </div>
                                    </div>
                                </div>
                            )}

                        {data.strengths && data.strengths.length > 0 && (
                            <div className={styles['page-home__grid-item-2']}>
                                <div className={styles['page-home__card']}>
                                    <h2 className={styles['page-home__card-title']}>Detected Strengths</h2>
                                    <ul className={styles['page-home__card-list']}>
                                        {data.strengths.map((s, i) => (
                                            <li key={i}>❍ {s}</li>
                                        ))}
                                    </ul>
                                </div>
                            </div>
                        )}

                        {data.issues && data.issues.length > 0 && (
                            <div className={styles['page-home__grid-item-3']}>
                                <div className={styles['page-home__card']}>
                                    <h2 className={styles['page-home__card-title']}>Detected Issues</h2>
                                    <ul className={styles['page-home__card-list']}>
                                        {data.issues.map((s, i) => (
                                            <li key={i}>❏ {s}</li>
                                        ))}
                                    </ul>
                                </div>
                            </div>
                        )}

                        {data.summary && (
                            <div className={styles['page-home__grid-item-4']}>
                                <div className={styles['page-home__card']}>
                                    <h2 className={styles['page-home__card-title']}>Summary</h2>
                                    <p className={styles['page-home__card-text']}>{data.summary}</p>
                                </div>
                            </div>
                        )}

                        {data.recommendations && data.recommendations.length > 0 && (
                            <div className={styles['page-home__grid-item-5']}>
                                <div className={styles['page-home__card']}>
                                    <h2 className={styles['page-home__card-title']}>Recommendations</h2>
                                    <ul className={styles['page-home__card-list']}>
                                        {data.recommendations.map((r, i) => (
                                            <li key={i}>{i + 1}. {r}</li>
                                        ))}
                                    </ul>
                                </div>
                            </div>
                        )}

                    </div>
                )
                }
            </div>
        </div>
    );
};

export default PageHome;