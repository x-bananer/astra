"use client";

import { useEffect, useState } from "react";
import styles from './page-home.module.css';
import Progress from '../_block/progress/progress';
import Button from '../_block/button/button';
import { useAuth } from "../auth/auth-provider";

const PageHome = () => {



    const auth = useAuth();

    const [greeting, setGreeting] = useState("");

    useEffect(() => {
        const h = new Date().getHours();

        let text = "";
        if (h >= 5 && h < 12) text = "Good morning";
        else if (h >= 12 && h < 18) text = "Good afternoon";
        else if (h >= 18 && h < 23) text = "Good evening";
        else text = "Good night";

        const name = auth?.user?.name || "";
        setGreeting(`${text} ${name.split(' ')?.[0] || name}`);
    }, [auth?.user]);

    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [teamNameInput, setTeamNameInput] = useState("");
    const [repoInput, setRepoInput] = useState("");
    const [gitlabRepoInput, setGitlabRepoInput] = useState("");
    

    async function handleCreateTeam() {
        await fetch("http://localhost:4000/groups/create", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify({ name: teamNameInput })
        });

        await auth.loadUser();
    }

    // useEffect(() => {

    //     async function load() {
    //         try {
    //             const res = await fetch("http://localhost:4000/analyze", {
    //                 method: "GET",
    //                 headers: {
    //                     "Accept": "application/json"
    //                 },
    //                 credentials: "include"
    //             });
    //             const json = await res.json();
    //             setData(json.analysis || null);
    //         } catch (e) {
    //             console.error("Failed to load:", e);
    //         } finally {
    //             setLoading(false);
    //         }
    //     }

    //     load();
    // }, []);

    return (
        <div className={styles['page-home']}>
            <div className={styles['page-home__header']}>
                <h1 className={styles['page-home__title']}>{greeting}</h1>
            </div>
            <div className={styles['page-home__content']}>
                <div className={styles['page-home__grid']}>
                    <div className={styles['page-home__card']}>
                        <h2 className={styles['page-home__card-title']}>Team Data</h2>
                        {auth?.user?.group?.id ?
                            <>
                                <div className={styles['page-home__card-row']}>
                                    Team name: {auth?.user?.group?.name}
                                </div>
                                <div className={styles['page-home__card-row']}>
                                    <ul className={styles['page-home__card-list']}>
                                        {auth?.user?.group?.members.map((member, index) => (
                                            <li key={index}>{index + 1}. {member.name}</li>
                                        ))}
                                    </ul>
                                </div>
                                <Button size="small" style={{ 'marginTop': '20px' }} variant="outline">
                                    + Add Teammate
                                </Button>

                            </> : <>
                                <div className={styles['page-home__card-row']}>
                                    You don’t have a team yet. You can create a new one or ask your teammates to add you to an existing team, allowing you to set up integrations and monitor your team’s activity.
                                </div>
                                <input
                                    type="text"
                                    placeholder="Team name"
                                    value={teamNameInput}
                                    onChange={(e) => setTeamNameInput(e.target.value)}
                                    className={styles['page-home__input']}
                                    style={{ 'marginTop': '20px' }}

                                />
                                <Button size="small" className={styles['page-home__card-button']} style={{ 'marginTop': '8px' }} variant="outline" onClick={handleCreateTeam}>
                                    + Create Team
                                </Button>
                            </>
                        }
                    </div>

                    <div className={styles['page-home__card']}>
                        <h2 className={styles['page-home__card-title']}>Integrations</h2>

                        {auth?.user?.group?.id ?
                            <div className={styles['page-home__card-grid']}>
                                <div className={styles['page-home__card-row']}>
                                    <div className={styles['page-home__card-text-accent']}>GitHub</div>

                                    {auth?.user?.group?.integrations?.some(i => i.provider === "github") ? (
                                        (() => {
                                            const git = auth.user.group.integrations.find(i => i.provider === "github");
                                            const [owner, repo] = git.repo_full_name.split("/");

                                            return (
                                                <>
                                                    <div style={{ 'height': '100%', 'display': 'flex', 'flexDirection': 'column' }}>
                                                        <span className={styles['page-home__card-text-secondary']}>
                                                            ASTRA reads your GitHub repository to gather activity data for analysis.
                                                            You can find the analysis on the "ASTRA Analysis" page.
                                                        </span>
                                                        <div style={{ marginTop: '4px' }}>
                                                            <div className={styles['page-home__card-text']}>
                                                                Connected repository: <span className={styles['page-home__card-text-accent']}>
                                                                    {repo}
                                                                </span>
                                                            </div>
                                                            <div className={styles['page-home__card-text']}>
                                                                Owner: <span className={styles['page-home__card-text-accent']}>
                                                                    {owner}
                                                                </span>
                                                            </div>
                                                        </div>
                                                        <div style={{ 'marginTop': 'auto', 'paddingTop': '12px' }}>
                                                            <input
                                                                type="text"
                                                                placeholder="Owner/Repo"
                                                                value={repoInput}
                                                                onChange={(e) => setRepoInput(e.target.value)}
                                                                className={styles['page-home__input']}
                                                                style={{ marginTop: '10px' }}
                                                            />

                                                            <Button
                                                                size="small"
                                                                className={styles['page-home__card-button']}
                                                                style={{ marginTop: '8px' }}
                                                                variant="outline"
                                                                onClick={() => {
                                                                    const param = encodeURIComponent(repoInput.trim());
                                                                    window.location.href =
                                                                        `http://localhost:4000/auth/github/login?repo=${param}`;
                                                                }}
                                                            >
                                                                Change Repository
                                                            </Button>
                                                        </div>
                                                    </div>
                                                </>
                                            );
                                        })()
                                    ) : (
                                    <div style={{ 'height': '100%', 'display': 'flex', 'flexDirection': 'column' }}>
                                        <span className={styles['page-home__card-text-secondary']}>
                                            Your team doesn’t have a GitHub integration yet. Connect a repository to start tracking activity.
                                        </span>
                                        <div style={{ 'marginTop': 'auto', 'paddingTop': '12px' }}>
                                            <input
                                                type="text"
                                                placeholder="Owner/Repo"
                                                value={repoInput}
                                                onChange={(e) => setRepoInput(e.target.value)}
                                                className={styles['page-home__input']}
                                                style={{ marginTop: '10px' }}
                                            />

                                            <Button
                                                size="small"
                                                className={styles['page-home__card-button']}
                                                style={{ marginTop: '8px' }}
                                                variant="primary"
                                                onClick={() => {
                                                    const param = encodeURIComponent(repoInput.trim());
                                                    window.location.href =
                                                        `http://localhost:4000/auth/github/login?repo=${param}`;
                                                }}
                                            >
                                                + Add GitHub Repo
                                            </Button>
                                        </div>
                                    </div>
                                    )}
                                </div>

                                <div className={styles['page-home__card-row']}>
                                    <div className={styles['page-home__card-text-accent']}>GitLab</div>

                                    {auth?.user?.group?.integrations?.some(i => i.provider === "gitlab") ? (
                                        (() => {
                                            const git = auth.user.group.integrations.find(i => i.provider === "gitlab");
                                            const [owner, repo] = git.repo_full_name.split("/");

                                            return (
                                                <>
                                                    <div style={{ 'height': '100%', 'display': 'flex', 'flexDirection': 'column' }}>
                                                        <span className={styles['page-home__card-text-secondary']}>
                                                            ASTRA reads your GitLab repository to gather activity data for analysis.
                                                            You can find the analysis on the "ASTRA Analysis" page.
                                                        </span>
                                                        <div style={{ marginTop: '4px' }}>
                                                            <div className={styles['page-home__card-text']}>
                                                                Connected repository: <span className={styles['page-home__card-text-accent']}>
                                                                    {repo}
                                                                </span>
                                                            </div>
                                                            <div className={styles['page-home__card-text']}>
                                                                Owner: <span className={styles['page-home__card-text-accent']}>
                                                                    {owner}
                                                                </span>
                                                            </div>
                                                        </div>
                                                        <div style={{ 'marginTop': 'auto', 'paddingTop': '12px' }}>
                                                            <input
                                                                type="text"
                                                                placeholder="Owner/Repo"
                                                                value={gitlabRepoInput}
                                                                onChange={(e) => setGitlabRepoInput(e.target.value)}
                                                                className={styles['page-home__input']}
                                                                style={{ marginTop: '10px' }}
                                                            />

                                                            <Button
                                                                size="small"
                                                                className={styles['page-home__card-button']}
                                                                style={{ marginTop: '8px' }}
                                                                variant="outline"
                                                                onClick={() => {
                                                                    const param = encodeURIComponent(gitlabRepoInput.trim());
                                                                    window.location.href =
                                                                        `http://localhost:4000/auth/gitlab/login?repo=${param}`;
                                                                }}
                                                            >
                                                                Change Repository
                                                            </Button>
                                                        </div>
                                                    </div>
                                                </>
                                            );
                                        })()
                                    ) : (
                                    <div style={{ 'height': '100%', 'display': 'flex', 'flexDirection': 'column' }}>
                                        <span className={styles['page-home__card-text-secondary']}>
                                            Your team doesn’t have a GitLab integration yet. Connect a repository to start tracking activity.
                                        </span>
                                        <div style={{ 'marginTop': 'auto', 'paddingTop': '12px' }}>
                                            <input
                                                type="text"
                                                placeholder="Owner/Repo"
                                                value={gitlabRepoInput}
                                                onChange={(e) => setGitlabRepoInput(e.target.value)}
                                                className={styles['page-home__input']}
                                                style={{ marginTop: '10px' }}
                                            />

                                            <Button
                                                size="small"
                                                className={styles['page-home__card-button']}
                                                style={{ marginTop: '8px' }}
                                                variant="primary"
                                                onClick={() => {
                                                    const param = encodeURIComponent(gitlabRepoInput.trim());
                                                    window.location.href =
                                                        `http://localhost:4000/auth/gitlab/login?repo=${param}`;
                                                }}
                                            >
                                                + Add GitLab Repo
                                            </Button>
                                        </div>
                                    </div>
                                    )}
                                </div>


                                <div className={styles['page-home__card-row']} style={{ 'height': '100%' }}>
                                    <div className={styles['page-home__card-text-accent']}>
                                        Trello
                                    </div>
                                    <div style={{ 'height': '100%', 'display': 'flex', 'flexDirection': 'column' }}>
                                        <span className={styles['page-home__card-text-secondary']}>
                                            Your team doesn’t have a Trello integration yet. Connect your board to start tracking activity.
                                        </span>
                                        <div style={{ 'marginTop': 'auto', 'paddingTop': '12px' }}>
                                            <Button size="small" className={styles['page-home__card-button']} variant="primary">
                                                + Add Trello Board
                                            </Button>
                                        </div>
                                    </div>
                                </div>

                                <div className={styles['page-home__card-row']} style={{ 'height': '100%' }}>
                                    <div className={styles['page-home__card-text-accent']}>
                                        Google Docs
                                    </div>
                                    <div style={{ 'height': '100%', 'display': 'flex', 'flexDirection': 'column' }}>
                                        <span className={styles['page-home__card-text-secondary']}>
                                            Your team doesn’t have a Google Docs integration yet. Connect your document to start tracking activity.
                                        </span>
                                        <div style={{ 'marginTop': 'auto', 'paddingTop': '12px' }}>
                                            <Button size="small" className={styles['page-home__card-button']} variant="primary">
                                                + Add Google Docs
                                            </Button>
                                        </div>
                                    </div>
                                </div>
                            </div> :
                            <div className={styles['page-home__card-row']}>
                                To set up, edit, or view your integrations, you need to belong to a team.
                                Create your own team using the "+ Create Team" button or join an existing one to start working with GitHub, GitLab, Trello, and Google Docs integrations and monitor your team’s activity..
                            </div>
                        }

                    </div>




                    {/* <div className={styles['page-home__grid-item-2']}>
                        <div className={styles['page-home__card']}>
                            <h2 className={styles['page-home__card-title']}>Detected Strengths</h2>
                            <ul className={styles['page-home__card-list']}>
                                {data.strengths.map((s, i) => (
                                    <li key={i}>❍ {s}</li>
                                ))}
                            </ul>
                        </div>
                    </div> */}



                    {/*  */}


                </div>


            </div>
        </div>
    );
};

export default PageHome;