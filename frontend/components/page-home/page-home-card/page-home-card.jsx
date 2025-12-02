import styles from './page-home-card.module.css';

import { useState } from 'react';

import { useAuth } from '../../auth/auth-provider';

import Button from '../../_block/button/button';

const INTEGRATIONS = {
    github: {
        title: "GitHub",
        description:
            "ASTRA reads your GitHub repository to gather activity data for analysis.",
        placeholder: "Owner/Repo",
        addLabel: "+ Add GitHub Repo",
        changeLabel: "Change Repository",
        buildUrl: (v) =>
            `http://localhost:4000/auth/github/login?repo=${encodeURIComponent(v)}`,
        renderConnected: (integration, styles) => {
            const [owner, repo] = integration.resource_ref.split("/");
            return (
                <>
                    <div className={styles['page-home-card__text']}>
                        Connected repository:{' '}
                        <span className={styles['page-home-card__text-accent']}>
                            {repo}
                        </span>
                    </div>
                    <div className={styles['page-home-card__text']}>
                        Owner:{' '}
                        <span className={styles['page-home-card__text-accent']}>
                            {owner}
                        </span>
                    </div>
                </>
            );
        }
    },

    gitlab: {
        title: "GitLab",
        description:
            "ASTRA reads your GitLab repository to gather activity data for analysis.",
        placeholder: "Owner/Repo",
        addLabel: "+ Add GitLab Repo",
        changeLabel: "Change Repository",
        buildUrl: (v) =>
            `http://localhost:4000/auth/gitlab/login?repo=${encodeURIComponent(v)}`,
        renderConnected: (integration, styles) => {
            const [owner, repo] = integration.resource_ref.split("/");
            return (
                <>
                    <div className={styles['page-home-card__text']}>
                        Connected repository:{' '}
                        <span className={styles['page-home-card__text-accent']}>
                            {repo}
                        </span>
                    </div>
                    <div className={styles['page-home-card__text']}>
                        Owner:{' '}
                        <span className={styles['page-home-card__text-accent']}>
                            {owner}
                        </span>
                    </div>
                </>
            );
        }
    },

    gdocs: {
        title: "Google Docs",
        description:
            "ASTRA reads metadata of your selected Google Docs document to gather activity information.",
        placeholder: "Google Docs document link",
        addLabel: "+ Add Link",
        changeLabel: "Change Link",
        buildUrl: (v) =>
            `http://localhost:4000/auth/gdocs/login?doc=${encodeURIComponent(v)}`,
        renderConnected: (integration, styles) => {
            const id = integration.resource_ref;
            return (
                <div className={styles['page-home-card__text']}>
                    Connected document:{' '}
                    <span className={styles['page-home-card__text-accent']}>
                        <a
                            target="_blank"
                            href={`https://docs.google.com/document/d/${id}/view`}
                        >
                            https://doc…
                        </a>
                    </span>
                </div>
            );
        }
    },

    trello: {
        title: "Trello",
        description:
            "Your team doesn’t have a Trello integration yet. Connect your board to start tracking activity.",
        placeholder: null,
        addLabel: "+ Add Trello Board",
        changeLabel: null,
        buildUrl: null,
        renderConnected: null
    }
};

const PageHomeCard = ({
    type
}) => {
    const auth = useAuth();
    const integration = auth?.user?.group?.integrations?.find(i => i.provider === type);
    const [inputValue, setInputValue] = useState("");

    const cfg = INTEGRATIONS[type];
    const isConnected = Boolean(integration);

    const title = cfg.title;
    const description = cfg.description;
    const placeholder = cfg.placeholder;

    const buttonLabel = isConnected ? cfg.changeLabel : cfg.addLabel;
    const buttonVariant = isConnected ? "outline" : "primary";

    const connectedBlock = isConnected
        ? cfg.renderConnected(integration, styles)
        : null;

    const handleSubmit = () => {
        if (!cfg.buildUrl) return;
        const trimmed = inputValue.trim();
        if (!trimmed) return;
        window.location.href = cfg.buildUrl(trimmed);
    };

    return (
        <div className={styles['page-home-card']}>

            <div className={styles['page-home-card__text-accent']}>
                {title}
            </div>

            <div style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>

                <span className={styles['page-home-card__text-secondary']}>
                    {description}
                </span>

                {connectedBlock && (
                    <div style={{ marginTop: '4px' }}>
                        {connectedBlock}
                    </div>
                )}

                <div style={{ marginTop: 'auto', paddingTop: '12px' }}>
                    {placeholder && (
                        <input
                            type="text"
                            placeholder={placeholder}
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                            className={styles['page-home-card__input']}
                            style={{ marginTop: '10px' }}
                        />
                    )}

                    <Button
                        size="small"
                        className={styles['page-home-card__button']}
                        style={{ marginTop: placeholder ? '8px' : '0' }}
                        variant={buttonVariant}
                        onClick={handleSubmit}
                    >
                        {buttonLabel}
                    </Button>
                </div>

            </div>
        </div>
    );
}

export default PageHomeCard;