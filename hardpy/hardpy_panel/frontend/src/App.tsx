// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from 'react';

import {
    Button,
    Navbar,
    Alignment,
    Classes,
    Colors,
    Menu,
    MenuItem,
    H2,
    Popover,
    Card
} from '@blueprintjs/core';

import StartStopButton from './button/StartStop';
import { SuiteList as SuiteList_v3 } from './hardpy_test_view/SuiteList_v3';
import { TestRunI } from './hardpy_test_view/SuiteList_v3';
import ProgressView from './progress/ProgressView';
import TestStatus from 'hardpy_test_view/TestStatus';
import ReloadAlert from './restart_alert/RestartAlert';
import PlaySound from 'hardpy_test_view/PlaySound';

import { useAllDocs } from 'use-pouchdb'

import './App.css';

/**
 * Main component of GUI
 */
function App(): JSX.Element {
    const [use_end_test_sound, setUseEndTestSound] = React.useState(false);
    const [use_debug_info, setUseDebugInfo] = React.useState(false);

    const [lastRunStatus, setLastRunStatus] = React.useState('');
    const [lastProgress, setProgress] = React.useState(0);
    const [isAuthenticated, setIsAuthenticated] = React.useState(true);

    const useWindowWide = (size: number) => {
        const [width, setWidth] = React.useState(0)

        React.useEffect(() => {
            function handleResize() {
                setWidth(window.innerWidth)
            }

            window.addEventListener("resize", handleResize)

            handleResize()

            return () => {
                window.removeEventListener("resize", handleResize)
            }
        }, [setWidth])

        return width > size
    }

    const ultrawide = useWindowWide(490)
    const wide = useWindowWide(400)

    const useRenderDb = () => {
        const { rows, state, loading, error } = useAllDocs({
            include_docs: true
          })

          React.useEffect(() => {
            if (state === 'error') {
              setIsAuthenticated(false);
            } else if (isAuthenticated === false) {
              setIsAuthenticated(true);
            }
          }, [state]);

          if (loading && rows.length === 0) {
            return  <Card style={{marginTop: '60px'}}>
                        <H2>Establishing a connection... 🧐🔎</H2>
                    </Card>
          }

          if (state === 'error') {
            return  <Card style={{marginTop: '60px'}}>
                        <H2>Database connection error. 🙅🏽‍♀️🚫</H2>
                        {error && <p>{error.message}</p>}
                    </Card>
          }

          if (rows.length === 0)
          {
            return  <Card style={{marginTop: '60px'}}>
                        <H2>No entries in the database 🫠</H2>
                    </Card>
          }

          /* Assume it is only one */
          const db_row = rows[0].doc as TestRunI
          const status = db_row.status
          if (status && (status != lastRunStatus))
          {
            setLastRunStatus(status)
          }

          const progress = db_row.progress
          if (progress && (progress != lastProgress))
          {
            setProgress(progress)
          }

          return (
            <div style={{marginTop: '40px'}}>
              {rows.map(row => (
                <div key={row.id} style={{display: 'flex', flexDirection: 'row'}}>
                    {(ultrawide || !use_debug_info) &&
                    <Card style={{
                        flexDirection: 'column',
                        padding: '20px',
                        flexGrow: 1,
                        flexShrink: 1,
                        marginTop: '20px',
                        marginBottom: '20px',
                    }}>
                        <SuiteList_v3 db_state={row.doc as TestRunI} defaultClose={!ultrawide}></SuiteList_v3>
                    </Card>
                    }
                    {use_debug_info &&
                    <Card style={{
                        flexDirection: 'column',
                        padding: '20px',
                        marginTop: '20px',
                        marginBottom: '20px',
                    }}>
                        <pre>{JSON.stringify(row.doc, null, 2)}</pre>
                    </Card>}
                </div>
              ))}
            </div>
          )
      };

    const renderSettingsMenu = () => {
        return (
            <Menu>
                <MenuItem
                    shouldDismissPopover={false}
                    text={use_end_test_sound ? 'Turn off the sound' : 'Turn on the sound'}
                    icon={use_end_test_sound ? 'volume-up' : 'volume-off'}
                    id='use_end_test_sound'
                    onClick={() => setUseEndTestSound(!use_end_test_sound)}
                />
                <MenuItem
                    shouldDismissPopover={false}
                    text={use_debug_info ? 'Turn off the debug mode' : 'Turn on the debug mode'}
                    icon={'bug'}
                    id='use_debug_info'
                    onClick={() => setUseDebugInfo(!use_debug_info)}
                />
            </Menu>
        );
    }

    return (
        <div className="App" style={{minWidth: '310px', margin: 'auto'}}>
            {/* Popout elements */}
            <ReloadAlert reload_timeout_s={3} />
            {/* <Notification /> */}

            {/* Header */}
            <Navbar fixedToTop={true} style={{ background: Colors.LIGHT_GRAY4, margin: 'auto'}}>
                <Navbar.Group align={Alignment.LEFT}>
                    <Navbar.Heading id={'main-heading'}>
                        <div className={'logo-smol'}></div>
                        {wide && <div>
                            <b>{ultrawide ? "HardPy Operator Panel" : "HardPy"}</b>
                        </div>
                        }
                    </Navbar.Heading>

                    { wide && <Navbar.Divider /> }

                    <Navbar.Heading id={'last-exec-heading'}>
                        <div>
                            Last run:
                        </div>
                    </Navbar.Heading>
                    <div id={'glob-test-status'}>
                        <TestStatus
                            status={lastRunStatus}
                        />
                        {use_end_test_sound && <PlaySound key="sound" status={lastRunStatus}/>}
                    </div>

                    <Navbar.Divider />
                </Navbar.Group>

                <Navbar.Group align={Alignment.RIGHT}>
                    <Popover content={renderSettingsMenu()}>
                        <Button className="bp3-minimal" icon="cog" />
                    </Popover>
                </Navbar.Group>
            </Navbar>

            {/* Tests panel */}
            <div className={Classes.DRAWER_BODY} style={{marginBottom: '60px'}}>
                {useRenderDb()}
            </div>

            {/* Footer */}

            <div className={Classes.DRAWER_FOOTER}
            style={{
                width: '100%',
                display: 'flex',
                flexDirection: 'row',
                position: 'fixed',
                bottom: 0,
                background: Colors.LIGHT_GRAY5,
                margin: 'auto',
            }}>
                <div style={{
                    flexDirection: 'column',
                    flexGrow: 1,
                    flexShrink: 1,
                    marginTop: 'auto',
                    marginBottom: 'auto',
                    padding: '20px'
                }}>
                    <ProgressView percentage={lastProgress} status={lastRunStatus} />
                </div>
                <div style={{flexDirection: 'column'}}>
                    <StartStopButton testing_status={lastRunStatus} is_authenticated={isAuthenticated}/>
                </div>
            </div>
        </div>
    );

}

export default App;
