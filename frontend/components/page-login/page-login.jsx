import styles from './page-login.module.css';

import AuthButton from '../auth/auth-button/auth-button';

const PageLogin = () => {
    return (
        <div className={styles['page-login']}>
            <div className={styles['page-login__main']}>
                <h1 className={styles['page-login__title']}>
                    ASTRA
                </h1>
                <p className={styles['page-login__subtitle']}>
                    Student Teamwork Regulating Assistant
                </p>
                <p className={styles['page-login__description']}>
                    <b>ASTRA</b> is a Metropolia service meant to help IT students organize their group work and understand team participation patterns. It analyzes activity from <b>GitHub</b>, <b>GitLab</b>, <b>Trello</b> and <b>Google Docs</b> to provide clear insights and AI-driven recommendations.
                </p>
                <ul className={styles['page-login__list']}>
                    <li>
                        <span className={styles['page-login__accent']}>
                            ✓
                        </span>

                        Team activity analytics
                    </li>

                    <li>
                        <span className={styles['page-login__accent']}>
                            ✓
                        </span> Project progress
                    </li>
                    <li>
                        <span className={styles['page-login__accent']}>
                            ✓
                        </span> Workload balance
                    </li>
                    <li>
                        <span className={styles['page-login__accent']}>
                            ✓
                        </span> AI-generated feedback
                    </li>
                </ul>
                <p className={styles['page-login__caption']}>Sign in now to access your team workspace!</p>
                <AuthButton />
            </div>
            <div className={styles['page-login__aside']}>
                <img src='/login-bg-2.png' alt='Background image' />
            </div>

        </div>
    );
};

export default PageLogin;