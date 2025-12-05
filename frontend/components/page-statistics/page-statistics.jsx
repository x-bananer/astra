"use client";

import { useEffect, useState } from "react";
import styles from './page-statistics.module.css';

const PageStatistics = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function load() {
            try {
                const res = await fetch("http://localhost:4000/analysis/statistics", {
                    method: "GET",
                    headers: {
                        "Accept": "application/json"
                    },
                    credentials: "include"
                });
                const json = await res.json();
                setData(json.data || null);
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
                <h1 className={styles['page-home__title']}>Statistics</h1>
                <p className={styles['page-home__subtitle']}>
                    These are the raw activity metrics for the last two weeks of your team’s work, collected and calculated every hour
                </p>
            </div>

            <div className={styles['page-home__content']}>
                {loading && (
                    <div className={styles['page-home__stub']}>
                        Fetching your team data...
                        <br></br>
                        This may take a moment! Please don't refresh the page
                    </div>
                )
                }

                {!data && !loading && (
                    <div className={styles['page-home__stub']}>
                        Oops! No data yet...
                    </div>
                )
                }

                {data && !loading && (
                    <>
                        {data.github &&
                            <div className={styles['page-home__box']}>
                                <h2 className={styles['page-home__box-title']}>
                                    GitHub
                                </h2>
                                <div className={styles['page-home__grid']}>
                                    <div className={styles['page-home__card']}>
                                        <div className={styles['page-home__card-title']}>Commits</div>
                                        <div className={styles['page-home__card-list']}>
                                            <div>Total commits: {data.github.commits_total}</div>
                                            <div>Contributors: {data.github.contributors_count}</div>
                                            <div>Busiest day: {data.github.busiest_day}</div>
                                            <div>Inactive for: {data.github.inactive_for_days} days</div>
                                        </div>
                                    </div>

                                    <div className={styles['page-home__card']}>
                                        <div className={styles['page-home__card-title']}>Commits by Author</div>
                                        <div className={styles['page-home__card-list']}>
                                            {Object.entries(data.github.contributors).map(([name, count]) => (
                                                <div key={name}>{name}: {count}</div>
                                            ))}
                                        </div>
                                    </div>

                                    <div className={styles['page-home__card']}>
                                        <div className={styles['page-home__card-title']}>Contribution Volume</div>
                                        <div className={styles['page-home__card-list']}>
                                            {Object.entries(data.github.contribution_volume).map(([name, value]) => (
                                                <div key={name}>{name}: {value}</div>
                                            ))}
                                        </div>
                                    </div>

                                    <div className={styles['page-home__card']}>
                                        <div className={styles['page-home__card-title']}>Contribution Share</div>
                                        <div className={styles['page-home__card-list']}>
                                            {Object.entries(data.github.volume_share).map(([name, value]) => (
                                                <div key={name}>{name}: {(value * 100).toFixed(1)}%</div>
                                            ))}
                                        </div>
                                    </div>

                                    <div className={styles['page-home__card']}>
                                        <div className={styles['page-home__card-title']}>Largest Contributor Share</div>
                                        <div className={styles['page-home__card-list']}>
                                            <div>{(data.github.largest_contributor_percentage * 100).toFixed(1)}%</div>
                                        </div>
                                    </div>

                                    <div className={styles['page-home__card']}>
                                        <div className={styles['page-home__card-title']}>Average Commit Size</div>
                                        <div className={styles['page-home__card-list']}>
                                            <div>{data.github.average_commit_size}</div>
                                        </div>
                                    </div>

                                    <div className={styles['page-home__card']}>
                                        <div className={styles['page-home__card-title']}>Average Commit Size by Author</div>
                                        <div className={styles['page-home__card-list']}>
                                            {Object.entries(data.github.average_commit_size_by_author).map(([name, size]) => (
                                                <div key={name}>{name}: {size}</div>
                                            ))}
                                        </div>
                                    </div>

                                    <div className={styles['page-home__card']}>
                                        <div className={styles['page-home__card-title']}>Largest Commit</div>
                                        <div className={styles['page-home__card-list']}>
                                            <div>Author: {data.github.largest_commit.author}</div>
                                            <div>Lines added: {data.github.largest_commit.additions}</div>
                                            <div>Lines removed: {data.github.largest_commit.deletions}</div>
                                            <div>Date: {data.github.largest_commit.date}</div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        }
                        {data.gitlab &&
                            <div className={styles['page-home__box']}>
                                <h2 className={styles['page-home__box-title']}>
                                    GitLab
                                </h2>
                                <div className={styles['page-home__grid']}>
                                    <div className={styles['page-home__card']}>
                                        <div className={styles['page-home__card-title']}>Commits</div>
                                        <div className={styles['page-home__card-list']}>
                                            <div>Total commits: {data.gitlab.commits_total}</div>
                                            <div>Contributors: {data.gitlab.contributors_count}</div>
                                            <div>Busiest day: {data.gitlab.busiest_day}</div>
                                            <div>Inactive for: {data.gitlab.inactive_for_days} days</div>
                                        </div>
                                    </div>

                                    <div className={styles['page-home__card']}>
                                        <div className={styles['page-home__card-title']}>Commits by Author</div>
                                        <div className={styles['page-home__card-list']}>
                                            {Object.entries(data.gitlab.contributors).map(([name, count]) => (
                                                <div key={name}>{name}: {count}</div>
                                            ))}
                                        </div>
                                    </div>

                                    <div className={styles['page-home__card']}>
                                        <div className={styles['page-home__card-title']}>Contribution Volume</div>
                                        <div className={styles['page-home__card-list']}>
                                            {Object.entries(data.gitlab.contribution_volume).map(([name, value]) => (
                                                <div key={name}>{name}: {value}</div>
                                            ))}
                                        </div>
                                    </div>

                                    <div className={styles['page-home__card']}>
                                        <div className={styles['page-home__card-title']}>Contribution Share</div>
                                        <div className={styles['page-home__card-list']}>
                                            {Object.entries(data.gitlab.volume_share).map(([name, value]) => (
                                                <div key={name}>{name}: {(value * 100).toFixed(1)}%</div>
                                            ))}
                                        </div>
                                    </div>

                                    <div className={styles['page-home__card']}>
                                        <div className={styles['page-home__card-title']}>Largest Contributor Share</div>
                                        <div className={styles['page-home__card-list']}>
                                            <div>{(data.gitlab.largest_contributor_percentage * 100).toFixed(1)}%</div>
                                        </div>
                                    </div>

                                    <div className={styles['page-home__card']}>
                                        <div className={styles['page-home__card-title']}>Average Commit Size</div>
                                        <div className={styles['page-home__card-list']}>
                                            <div>{data.gitlab.average_commit_size}</div>
                                        </div>
                                    </div>

                                    <div className={styles['page-home__card']}>
                                        <div className={styles['page-home__card-title']}>Average Commit Size by Author</div>
                                        <div className={styles['page-home__card-list']}>
                                            {Object.entries(data.gitlab.average_commit_size_by_author).map(([name, size]) => (
                                                <div key={name}>{name}: {size}</div>
                                            ))}
                                        </div>
                                    </div>

                                    <div className={styles['page-home__card']}>
                                        <div className={styles['page-home__card-title']}>Largest Commit</div>
                                        <div className={styles['page-home__card-list']}>
                                            <div>Author: {data.gitlab.largest_commit.author}</div>
                                            <div>Lines added: {data.gitlab.largest_commit.additions}</div>
                                            <div>Lines removed: {data.gitlab.largest_commit.deletions}</div>
                                            <div>Date: {data.gitlab.largest_commit.date}</div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        }
                        {data.gdocs &&
                            <div className={styles['page-home__box']}>
                                <h2 className={styles['page-home__box-title']}>
                                    Google Docs
                                </h2>
                                <div className={styles['page-home__grid']}>
                                    <div className={styles['page-home__card']}>
                                        <div className={styles['page-home__card-title']}>Revisions</div>
                                        <div className={styles['page-home__card-list']}>
                                            <div>Total revisions: {data.gdocs.total_revisions}</div>
                                            <div>Contributors: {data.gdocs.contributors_count}</div>
                                            <div>Last edit: {data.gdocs.last_edit}</div>
                                            <div>Inactive for: {data.gdocs.inactive_for_days} days</div>
                                        </div>
                                    </div>

                                    <div className={styles['page-home__card']}>
                                        <div className={styles['page-home__card-title']}>Activity by Day</div>
                                        <div className={styles['page-home__card-list']}>
                                            {Object.entries(data.gdocs.activity_by_day).map(([day, count]) => (
                                                <div key={day}>{day}: {count}</div>
                                            ))}
                                        </div>
                                    </div>

                                    <div className={styles['page-home__card']}>
                                        <div className={styles['page-home__card-title']}>Activity by Hour</div>
                                        <div className={styles['page-home__card-list']}>
                                            {Object.entries(data.gdocs.activity_by_hour).map(([hour, count]) => (
                                                <div key={hour}>{hour}: {count}</div>
                                            ))}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        }
                    </>
                )}
            </div>
        </div>
    );
};

export default PageStatistics;