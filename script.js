document.addEventListener('DOMContentLoaded', () => {
    const assetPath = 'assets/ShooterGame/'; 

    // ... (Your huge asset list remains unchanged, pasted for brevity) ...
    const agentIcons = {
        astra: { path: `${assetPath}TX_Killfeed_Astra.png`, name: "Astra" },
        breach: { path: `${assetPath}TX_Killfeed_Breach.png`, name: "Breach" },
        brimstone: { path: `${assetPath}TX_Killfeed_Brimstone.png`, name: "Brimstone" },
        chamber: { path: `${assetPath}TX_Killfeed_Chamber.png`, name: "Chamber" },
        clove: { path: `${assetPath}TX_Killfeed_Clove.png`, name: "Clove" },
        cypher: { path: `${assetPath}TX_Killfeed_Cypher.png`, name: "Cypher" },
        deadlock: { path: `${assetPath}TX_Killfeed_Deadlock.png`, name: "Deadlock" },
        fade: { path: `${assetPath}TX_Killfeed_Fade.png`, name: "Fade" },
        gekko: { path: `${assetPath}TX_Killfeed_Gekko.png`, name: "Gekko" },
        iso: { path: `${assetPath}TX_Killfeed_Iso.png`, name: "Iso" },
        jett: { path: `${assetPath}TX_Killfeed_Jett.png`, name: "Jett" },
        kayo: { path: `${assetPath}TX_Killfeed_KAYO.png`, name: "KAY/O" },
        killjoy: { path: `${assetPath}TX_Killfeed_Killjoy1.png`, name: "Killjoy" },
        neon: { path: `${assetPath}TX_Killfeed_Neon.png`, name: "Neon" },
        omen: { path: `${assetPath}TX_Killfeed_Omen.png`, name: "Omen" },
        phoenix: { path: `${assetPath}TX_Killfeed_Phoenix.png`, name: "Phoenix" },
        raze: { path: `${assetPath}TX_Killfeed_Raze.png`, name: "Raze" },
        reyna: { path: `${assetPath}TX_Killfeed_Reyna.png`, name: "Reyna" },
        sage: { path: `${assetPath}TX_Killfeed_Sage1.png`, name: "Sage" },
        skye: { path: `${assetPath}TX_Killfeed_Skye.png`, name: "Skye" },
        sova: { path: `${assetPath}TX_Killfeed_Sova1.png`, name: "Sova" },
        viper: { path: `${assetPath}TX_Killfeed_Viper.png`, name: "Viper" },
        yoru: { path: `${assetPath}TX_Killfeed_Yoru.png`, name: "Yoru" },
        pine: { path: `${assetPath}TX_Killfeed_Pine.png`, name: "Veto" },
        vyse: { path: `${assetPath}TX_Killfeed_Vyse.png`, name: "Vyse" },
        tejo: { path: `${assetPath}TX_Killfeed_Tejo.png`, name: "Tejo" },
        mage: { path: `${assetPath}TX_Killfeed_Mage.png`, name: "Harbor" },
        waylay: { path: `${assetPath}TX_Killfeed_Waylay.png`, name: "Waylay (Iso)" },
        sym: { path: `${assetPath}TX_Killfeed_Sym.png`, name: "Veto (Ult)" },
    };
    
    const weaponIcons = {
        classic: { path: `${assetPath}TX_Hud_Pistol_Classic.png`, name: "Classic" },
        ghost: { path: `${assetPath}TX_Hud_Pistol_Luger.png`, name: "Ghost" },
        shorty: { path: `${assetPath}TX_Hud_Pistol_Slim.png`, name: "Shorty" },
        frenzy: { path: `${assetPath}TX_Hud_Pistol_AutoPistol.png`, name: "Frenzy" },
        sheriff: { path: `${assetPath}TX_Hud_Pistol_Sheriff.png`, name: "Sheriff" },
        stinger: { path: `${assetPath}TX_Hud_SMGs_Vector.png`, name: "Stinger" },
        spectre: { path: `${assetPath}TX_Hud_SMGs_Ninja.png`, name: "Spectre" },
        bucky: { path: `${assetPath}TX_Hud_Shotguns_Pump.png`, name: "Bucky" },
        judge: { path: `${assetPath}TX_Hud_Shotguns_Persuader.png`, name: "Judge" },
        bulldog: { path: `${assetPath}TX_Hud_Rifles_Burst.png`, name: "Bulldog" },
        guardian: { path: `${assetPath}TX_Hud_Rifles_DMR.png`, name: "Guardian" },
        phantom: { path: `${assetPath}TX_Hud_Rifles_Ghost.png`, name: "Phantom" },
        vandal: { path: `${assetPath}TX_Hud_Rifles_Volcano.png`, name: "Vandal" },
        marshal: { path: `${assetPath}TX_Hud_Sniper_Bolt.png`, name: "Marshal" },
        operator: { path: `${assetPath}TX_Hud_Sniper_Operater.png`, name: "Operator" },
        ares: { path: `${assetPath}TX_Hud_LMG.png`, name: "Ares" },
        odin: { path: `${assetPath}TX_Hud_HMG.png`, name: "Odin" },
        knife: { path: `${assetPath}TX_Hud_Knife_Standard.png`, name: "Knife" },
        aftershock: { path: `${assetPath}TX_Breach_FusionBlast.png`, name: "Breach: Aftershock" },
        incendiary: { path: `${assetPath}TX_Sarge_MolotovLauncher.png`, name: "Brimstone: Incendiary" },
        orbital_strike: { path: `${assetPath}TX_Sarge_OrbitalStrike.png`, name: "Brimstone: Orbital Strike" },
        headhunter: { path: `${assetPath}TX_Hud_Deadeye_Q_Pistol.png`, name: "Chamber: Headhunter" },
        tour_de_force: { path: `${assetPath}TX_Hud_Deadeye_X_GiantSlayer.png`, name: "Chamber: Tour de Force" },
        mosh_pit: { path: `${assetPath}TX_Aggrobot_MoshPit.png`, name: "Gekko: Mosh Pit" },
        thrash: { path: `${assetPath}TX_Aggrobot_Thrash.png`, name: "Gekko: Thrash" },
        blade_storm: { path: `${assetPath}TX_Wushu_Daggers.png`, name: "Jett: Blade Storm" },
        fragment: { path: `${assetPath}TX_Hud_Icons_Abilities_EMP.png`, name: "KAY/O: FRAG/MENT" },
        nanoswarm: { path: `${assetPath}TX_KJ_Bees.png`, name: "Killjoy: Nanoswarm" },
        turret: { path: `${assetPath}tx_KJ_turret.png`, name: "Killjoy: Turret" },
        hot_hands: { path: `${assetPath}TX_Pheonix_Molotov.png`, name: "Phoenix: Hot Hands" },
        blaze: { path: `${assetPath}TX_Pheonix_FireWall.png`, name: "Phoenix: Blaze" },
        boom_bot: { path: `${assetPath}TX_Clay_Boomba.png`, name: "Raze: Boom Bot" },
        blast_pack: { path: `${assetPath}TX_Clay_Satchel.png`, name: "Raze: Blast Pack" },
        paint_shells: { path: `${assetPath}TX_Clay_ClusterBomb.png`, name: "Raze: Paint Shells" },
        showstopper: { path: `${assetPath}TX_Clay_RocketLauncher.png`, name: "Raze: Showstopper" },
        shock_bolt: { path: `${assetPath}TX_Hunter_ShockArrow.png`, name: "Sova: Shock Bolt" },
        hunters_fury: { path: `${assetPath}TX_Hunter_BowBlast.png`, name: "Sova: Hunter's Fury" },
        snake_bite: { path: `${assetPath}TX_Pandemic_AcidLauncher.png`, name: "Viper: Snake Bite" },
        poison_cloud: { path: `${assetPath}TX_Pandemic_SmokeGrenade.png`, name: "Viper: Poison Cloud" },
        toxic_screen: { path: `${assetPath}TX_Pandemic_SmokeWall.png`, name: "Viper: Toxic Screen" },
        guided_salvo: { path: `${assetPath}TX_Tejo_GuidedSalvo.png`, name: "Tejo: Guided Salvo" },
        armageddon: { path: `${assetPath}TX_Tejo_Armageddon.png`, name: "Tejo: Armageddon" },
    };

    const killTypeIcons = {
        headshot: { path: `${assetPath}TX_Kilfeed_Headshot.png`, name: "Headshot" },
        wallbang: { path: `${assetPath}TX_Kilfeed_WallPen.png`, name: "Wallbang" },
        spike: { path: `${assetPath}TX_Killfeed_SpikeExplosion.png`, name: "Spike" },
    };

    let state = {
        killFeed: [], 
        history: [],    
        currentlyEditingId: null,
        draggedElementId: null
    };

    const captureAreaWrapper = document.getElementById('capture-area-wrapper'); 
    const killFeedContainer = document.getElementById('killfeed-container');
    const killTemplate = document.getElementById('kill-entry-template');
    const attackerNameInput = document.getElementById('attacker-name');
    const attackerAgentSelect = document.getElementById('attacker-agent');
    const multikillSelect = document.getElementById('multikill-count'); 
    const weaponSelect = document.getElementById('weapon');
    const killTypeContainer = document.getElementById('kill-type-container'); 
    const victimNameInput = document.getElementById('victim-name');
    const victimAgentSelect = document.getElementById('victim-agent');
    const separatorTextInput = document.getElementById('separator-text'); 
    const addControls = document.getElementById('add-controls');
    const editControls = document.getElementById('edit-controls');
    const addKillButton = document.getElementById('add-kill-btn');
    const addSeparatorButton = document.getElementById('add-separator-btn'); 
    const updateKillButton = document.getElementById('update-kill-btn');
    const cancelEditButton = document.getElementById('cancel-edit-btn');
    const undoButton = document.getElementById('undo-btn');
    const clearFeedButton = document.getElementById('clear-feed-btn');
    const downloadPngButton = document.getElementById('download-png-btn'); 
    const previewAreaBg = document.getElementById('preview-area-bg'); 
    const panelTitle = document.getElementById('panel-title');

    // Style Settings
    const styleWidth = document.getElementById('style-width');
    const styleHeight = document.getElementById('style-height');
    const styleBgColor = document.getElementById('style-bg-color');
    const styleBgOpacity = document.getElementById('style-bg-opacity');
    const styleBorderAngle = document.getElementById('style-border-angle');
    const styleBorderStart = document.getElementById('style-border-start');
    const styleBorderEnd = document.getElementById('style-border-end');
    const styleBorderWidth = document.getElementById('style-border-width');
    const styleDashColor = document.getElementById('style-dash-color');
    const styleGlowEnabled = document.getElementById('style-glow-enabled');
    const styleGlowColor = document.getElementById('style-glow-color');
    const styleGlowIntensity = document.getElementById('style-glow-intensity');
    const styleAttackerColor = document.getElementById('style-attacker-color');
    const styleVictimColor = document.getElementById('style-victim-color');
    const styleIconColor = document.getElementById('style-icon-color');
    const presetDefault = document.getElementById('preset-default');
    const presetValAlly = document.getElementById('preset-val-ally');
    const presetValEnemy = document.getElementById('preset-val-enemy');
    const styleBgImageInput = document.getElementById('style-bg-image-input');
    const clearBgImageBtn = document.getElementById('clear-bg-image-btn');
    const styleBgPosX = document.getElementById('style-bg-pos-x');
    const styleBgPosY = document.getElementById('style-bg-pos-y');
    const styleBgSize = document.getElementById('style-bg-size');

    // Labels
    const displayPosX = document.getElementById('display-pos-x');
    const displayPosY = document.getElementById('display-pos-y');
    const displayScale = document.getElementById('display-scale');

    function hexToRgba(hex, opacityPercent) {
        const r = parseInt(hex.slice(1, 3), 16);
        const g = parseInt(hex.slice(3, 5), 16);
        const b = parseInt(hex.slice(5, 7), 16);
        return `rgba(${r}, ${g}, ${b}, ${opacityPercent / 100})`;
    }

    function hexToRgbaWithAlpha(hex, alpha) {
         const r = parseInt(hex.slice(1, 3), 16);
        const g = parseInt(hex.slice(3, 5), 16);
        const b = parseInt(hex.slice(5, 7), 16);
        return `rgba(${r}, ${g}, ${b}, ${alpha})`;
    }

    function updateStyles() {
        const root = document.documentElement;
        
        // Update Labels
        displayPosX.textContent = styleBgPosX.value + '%';
        displayPosY.textContent = styleBgPosY.value + '%';
        displayScale.textContent = styleBgSize.value + '%';

        root.style.setProperty('--kf-width', `${styleWidth.value}px`);
        root.style.setProperty('--kf-height', `${styleHeight.value}px`);
        root.style.setProperty('--kf-border-width', `${styleBorderWidth.value}px`);
        root.style.setProperty('--kf-border-angle', `${styleBorderAngle.value}deg`);
        root.style.setProperty('--kf-border-start', styleBorderStart.value);
        root.style.setProperty('--kf-border-end', styleBorderEnd.value);
        root.style.setProperty('--kf-bg-color', hexToRgba(styleBgColor.value, styleBgOpacity.value));
        root.style.setProperty('--kf-dash-color', styleDashColor.value);
        root.style.setProperty('--kf-attacker-color', styleAttackerColor.value);
        root.style.setProperty('--kf-victim-color', styleVictimColor.value);
        root.style.setProperty('--kf-icon-color', styleIconColor.value);
        
        // BG Props
        root.style.setProperty('--kf-bg-pos-x', `${styleBgPosX.value}%`);
        root.style.setProperty('--kf-bg-pos-y', `${styleBgPosY.value}%`);
        root.style.setProperty('--kf-bg-size', `${styleBgSize.value}%`);

        if (styleGlowEnabled.checked) {
            const glowSize = styleGlowIntensity.value + 'px';
            const glowColor = hexToRgbaWithAlpha(styleGlowColor.value, 0.6); 
            root.style.setProperty('--kf-shadow', `0 0 ${glowSize} ${glowColor}`);
        } else {
            root.style.setProperty('--kf-shadow', 'none');
        }
    }

    styleBgImageInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                const imgUrl = `url('${e.target.result}')`;
                document.documentElement.style.setProperty('--kf-bg-image', imgUrl);
                clearBgImageBtn.classList.remove('hidden');
            };
            reader.readAsDataURL(file);
        }
    });

    clearBgImageBtn.addEventListener('click', () => {
        document.documentElement.style.setProperty('--kf-bg-image', 'none');
        styleBgImageInput.value = ''; 
        clearBgImageBtn.classList.add('hidden');
    });

    [styleWidth, styleHeight, styleBgColor, styleBgOpacity, styleBorderWidth, styleBorderAngle, styleBorderStart, styleBorderEnd, 
     styleDashColor, styleGlowEnabled, styleGlowColor, styleGlowIntensity,
     styleAttackerColor, styleVictimColor, styleIconColor,
     styleBgPosX, styleBgPosY, styleBgSize].forEach(el => {
        if(el) el.addEventListener('input', updateStyles);
    });

    function applyPreset(type) {
        if (type === 'default') {
            styleBgColor.value = "#000000"; styleBgOpacity.value = 100;
            styleBorderAngle.value = 180;
            styleBorderStart.value = "#8e00e7";
            styleBorderEnd.value = "#420067";
            styleDashColor.value = "#8e00e7";
            styleGlowEnabled.checked = true;
            styleGlowColor.value = "#8e00e7";
            styleGlowIntensity.value = 10;
            styleAttackerColor.value = "#ffffff";
            styleVictimColor.value = "#ffffff";
            styleIconColor.value = "#ffffff";
        } else if (type === 'ally') {
            styleBgColor.value = "#000000"; styleBgOpacity.value = 70;
            styleBorderAngle.value = 90;
            styleBorderStart.value = "#00ffff";
            styleBorderEnd.value = "#008080";
            styleDashColor.value = "#00ffff";
            styleGlowEnabled.checked = false;
            styleAttackerColor.value = "#ffffff";
            styleVictimColor.value = "#ffffff";
            styleIconColor.value = "#ffffff";
        } else if (type === 'enemy') {
            styleBgColor.value = "#000000"; styleBgOpacity.value = 70;
            styleBorderAngle.value = 90;
            styleBorderStart.value = "#ff4655";
            styleBorderEnd.value = "#800000";
            styleDashColor.value = "#ff4655";
            styleGlowEnabled.checked = false;
            styleAttackerColor.value = "#ffffff";
            styleVictimColor.value = "#ffffff";
            styleIconColor.value = "#ffffff";
        }
        updateStyles();
    }

    if(presetDefault) presetDefault.addEventListener('click', () => applyPreset('default'));
    if(presetValAlly) presetValAlly.addEventListener('click', () => applyPreset('ally'));
    if(presetValEnemy) presetValEnemy.addEventListener('click', () => applyPreset('enemy'));


    // --- Core Logic ---

    function saveState() {
        state.history.push(JSON.parse(JSON.stringify(state.killFeed)));
        if (state.history.length > 20) state.history.shift(); 
    }

    function getKillDataFromForm() {
        const selectedKillTypes = [];
        killTypeContainer.querySelectorAll('input[type="checkbox"]:checked').forEach(checkbox => {
            selectedKillTypes.push(checkbox.value);
        });
        return {
            type: 'kill', 
            attackerName: attackerNameInput.value,
            attackerAgent: attackerAgentSelect.value,
            victimName: victimNameInput.value,
            victimAgent: victimAgentSelect.value,
            weapon: weaponSelect.value,
            killTypes: selectedKillTypes, 
            multikillCount: parseInt(multikillSelect.value, 10),
            id: state.currentlyEditingId || Date.now() 
        };
    }

    function populateFormFromKill(kill) {
        attackerNameInput.value = kill.attackerName;
        attackerAgentSelect.value = kill.attackerAgent;
        victimNameInput.value = kill.victimName;
        victimAgentSelect.value = kill.victimAgent;
        weaponSelect.value = kill.weapon;
        multikillSelect.value = kill.multikillCount;
        killTypeContainer.querySelectorAll('input[type="checkbox"]').forEach(checkbox => checkbox.checked = false);
        if (kill.killTypes) {
            kill.killTypes.forEach(type => {
                const checkbox = killTypeContainer.querySelector(`input[value="${type}"]`);
                if (checkbox) checkbox.checked = true;
            });
        }
    }

    function resetForm() {
        victimNameInput.value = "victim";
    }

    function setEditMode(isEditing) {
        if (isEditing) {
            addControls.classList.add('hidden');
            editControls.classList.remove('hidden');
            panelTitle.textContent = "Edit Kill Details";
            panelTitle.classList.add('text-blue-400');
        } else {
            addControls.classList.remove('hidden');
            editControls.classList.add('hidden');
            state.currentlyEditingId = null;
            panelTitle.textContent = "Add New Kill";
            panelTitle.classList.remove('text-blue-400');
            resetForm(); 
        }
    }

    function render() {
        killFeedContainer.innerHTML = ''; 

        state.killFeed.forEach((kill) => {
            const killRow = killTemplate.content.cloneNode(true).firstElementChild;
            killRow.dataset.id = kill.id; 

            if (kill.type === 'separator') {
                killRow.classList.add('separator');
                const textEl = killRow.querySelector('.separator-text');
                textEl.textContent = kill.text;
            } else {
                const multikillColumn = killRow.querySelector('.multikill-column');
                if (kill.multikillCount > 1) {
                    for (let i = 0; i < kill.multikillCount; i++) {
                        const dash = document.createElement('div');
                        dash.className = 'multikill-dash';
                        multikillColumn.appendChild(dash);
                    }
                }

                const attackerIconEl = killRow.querySelector('.agent-icon.attacker');
                const attackerNameEl = killRow.querySelector('.attacker-name');
                const weaponIconEl = killRow.querySelector('.weapon-icon');
                const killTypeIconsContainer = killRow.querySelector('.kill-type-icons'); 
                const victimNameEl = killRow.querySelector('.victim-name');
                const victimIconEl = killRow.querySelector('.agent-icon.victim');

                attackerIconEl.src = agentIcons[kill.attackerAgent]?.path || agentIcons.cypher.path;
                attackerNameEl.textContent = kill.attackerName;
                weaponIconEl.src = weaponIcons[kill.weapon]?.path || weaponIcons.vandal.path;
                victimIconEl.src = agentIcons[kill.victimAgent]?.path || agentIcons.jett.path;
                victimNameEl.textContent = kill.victimName;

                killTypeIconsContainer.innerHTML = ''; 
                if (kill.killTypes) {
                    kill.killTypes.forEach(type => {
                        if (killTypeIcons[type]) {
                            const icon = document.createElement('img');
                            icon.src = killTypeIcons[type].path;
                            icon.className = 'kill-type-icon';
                            killTypeIconsContainer.appendChild(icon);
                        }
                    });
                }
            }

            if (kill.id === state.currentlyEditingId) {
                killRow.classList.add('selected');
            }

            killRow.addEventListener('click', (e) => {
                e.stopPropagation(); 
                if (kill.type === 'separator') return; 
                state.currentlyEditingId = kill.id;
                populateFormFromKill(kill);
                setEditMode(true);
                render(); 
            });

            killRow.addEventListener('dragstart', (e) => {
                state.draggedElementId = kill.id;
                setTimeout(() => killRow.classList.add('dragging'), 0);
            });
            killRow.addEventListener('dragend', () => {
                killRow.classList.remove('dragging');
                state.draggedElementId = null;
            });

            killFeedContainer.append(killRow);
        });
    }

    killFeedContainer.addEventListener('dragover', e => { e.preventDefault(); });
    killFeedContainer.addEventListener('drop', e => {
        e.preventDefault();
        if (!state.draggedElementId) return;
        const afterElement = getDragAfterElement(killFeedContainer, e.clientY);
        saveState(); 
        const draggedKillIndex = state.killFeed.findIndex(k => k.id == state.draggedElementId);
        const [draggedKill] = state.killFeed.splice(draggedKillIndex, 1);
        if (afterElement == null) {
            state.killFeed.push(draggedKill);
        } else {
            const dropIndex = state.killFeed.findIndex(k => k.id == afterElement.dataset.id);
            state.killFeed.splice(dropIndex, 0, draggedKill);
        }
        render(); 
    });

    function getDragAfterElement(container, y) {
        const draggableElements = [...container.querySelectorAll('.kill-row:not(.dragging)')];
        return draggableElements.reduce((closest, child) => {
            const box = child.getBoundingClientRect();
            const offset = y - box.top - box.height / 2;
            if (offset < 0 && offset > closest.offset) return { offset: offset, element: child };
            else return closest;
        }, { offset: Number.NEGATIVE_INFINITY }).element;
    }

    previewAreaBg.addEventListener('click', (e) => {
        if (e.target === previewAreaBg || e.target === captureAreaWrapper) {
            setEditMode(false);
            render();
        }
    });

    addKillButton.addEventListener('click', () => {
        saveState(); 
        const newKill = getKillDataFromForm();
        newKill.id = Date.now(); 
        state.killFeed.push(newKill);
        render();
    });

    addSeparatorButton.addEventListener('click', () => {
        saveState();
        const newSeparator = {
            type: 'separator',
            text: separatorTextInput.value, 
            id: Date.now()
        };
        state.killFeed.push(newSeparator);
        separatorTextInput.value = ''; 
        render();
    });

    updateKillButton.addEventListener('click', () => {
        saveState(); 
        const updatedKillData = getKillDataFromForm();
        state.killFeed = state.killFeed.map(kill => {
            if (kill.id === state.currentlyEditingId) return updatedKillData; 
            return kill; 
        });
        setEditMode(false); 
        render();
    });

    cancelEditButton.addEventListener('click', () => {
        setEditMode(false);
        render(); 
    });

    undoButton.addEventListener('click', () => {
        if (state.history.length === 0) return; 
        state.killFeed = state.history.pop();
        setEditMode(false);
        render();
    });

    clearFeedButton.addEventListener('click', () => {
        if (state.killFeed.length === 0) return; 
        saveState(); 
        state.killFeed = []; 
        setEditMode(false);
        render();
    });

    downloadPngButton.addEventListener('click', () => {
        alert("This feature is currently Work In Progress (WIP) due to browser security restrictions. Please use your system's screenshot tool (Win+Shift+S or Cmd+Shift+4) to capture the preview area.");
    });

    function populateSelect(selectElement, optionsMap) {
        selectElement.innerHTML = ''; 
        const sortedKeys = Object.keys(optionsMap).sort((a, b) => 
            optionsMap[a].name.localeCompare(optionsMap[b].name)
        );
        sortedKeys.forEach(key => {
            const option = document.createElement('option');
            option.value = key;
            option.textContent = optionsMap[key].name;
            selectElement.appendChild(option);
        });
    }

    function populateKillTypes(container, optionsMap) {
        container.innerHTML = '';
        Object.keys(optionsMap).forEach(key => {
            const label = document.createElement('label');
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.value = key;
            label.appendChild(checkbox);
            label.appendChild(document.createTextNode(optionsMap[key].name));
            container.appendChild(label);
        });
    }

    function initialize() {
        populateSelect(attackerAgentSelect, agentIcons);
        populateSelect(victimAgentSelect, agentIcons);
        populateSelect(weaponSelect, weaponIcons);
        populateKillTypes(killTypeContainer, killTypeIcons); 
        render(); 
        resetForm(); 
        updateStyles(); 
    }

    initialize(); 
});