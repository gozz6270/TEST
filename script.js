const nameForm = document.getElementById('name-form');
const nameScreen = document.getElementById('name-screen');
const storyScreen = document.getElementById('story-screen');
const storyLog = document.getElementById('story-log');
const choiceList = document.getElementById('choice-list');

const state = {
  heroName: '',
  alliedRangers: false,
  sacredRelic: false,
  villageInspired: false,
};

const scenes = {
  village: {
    description: (ctx) =>
      `${ctx.heroName}는 브린델 마을의 중앙 광장에 섰다. 하늘을 가득 메운 잿빛 구름 아래, 장로는 용의 습격으로 황폐해진 왕국을 구해 달라고 간청한다. 선택은 오로지 그대의 몫이다.`,
    choices: [
      {
        text: '숲의 순찰대와 합류해 용의 흔적을 추적한다.',
        next: 'forestCamp',
        effect: (ctx) => {
          ctx.alliedRangers = true;
        },
      },
      {
        text: '폐허가 된 성소를 조사해 고대의 힘을 찾는다.',
        next: 'ruinedChapel',
      },
      {
        text: '마을에 남아 사람들의 사기를 북돋운다.',
        next: 'villageDefense',
        effect: (ctx) => {
          ctx.villageInspired = true;
        },
      },
    ],
  },
  forestCamp: {
    description: (ctx) =>
      `어스름한 숲 속, 순찰대장 엘리온은 ${ctx.heroName}에게 용이 북쪽 산맥으로 날아갔다는 보고를 전한다. 그들은 숨어 있는 정찰병을 도와줄지, 즉시 산맥으로 향할지 결정을 기다린다.`,
    choices: [
      {
        text: '숨어 있던 정찰병을 구출해 정보를 얻는다.',
        next: 'hiddenScout',
      },
      {
        text: '시간을 아끼기 위해 곧장 산길로 향한다.',
        next: 'mountainPass',
      },
    ],
  },
  hiddenScout: {
    description: (ctx) =>
      `정찰병은 목숨을 구해 준 ${ctx.heroName}에게 용이 마법 봉인을 두려워한다는 사실을 전한다. 그는 오래된 봉인 주문이 성소의 유물에 깃들어 있다고 귀띔한다.`,
    choices: [
      {
        text: '유물을 찾기 위해 폐허 성소로 향한다.',
        next: 'ruinedChapel',
      },
      {
        text: '얻은 정보로 곧장 산길을 오른다.',
        next: 'mountainPass',
      },
    ],
  },
  ruinedChapel: {
    description: (ctx) =>
      `허물어진 성소의 제단 아래에서 ${ctx.heroName}는 황금빛 성배를 발견한다. 성배에는 용의 숨결을 잠재울 고대의 봉인이 깃들어 있다.`,
    choices: [
      {
        text: '성배를 손에 넣고 산맥으로 떠난다.',
        next: 'mountainPass',
        effect: (ctx) => {
          ctx.sacredRelic = true;
        },
      },
      {
        text: '성소 깊숙한 지하 묘실을 더 수색한다.',
        next: 'crypt',
        effect: (ctx) => {
          ctx.sacredRelic = true;
        },
      },
    ],
  },
  crypt: {
    description: (ctx) =>
      `지하 묘실에서 ${ctx.heroName}는 고대 기사단의 일지를 발견한다. 일지에는 용이 말과 협상을 이해한다는 사실이 기록되어 있다.`,
    choices: [
      {
        text: '일지를 품고 산맥으로 향한다.',
        next: 'mountainPass',
      },
    ],
  },
  villageDefense: {
    description: (ctx) =>
      `${ctx.heroName}는 주민들과 밤새 방벽을 보수하고, 희망의 노래를 불러 사기를 올린다. 사람들은 영웅의 결의를 보며 다시 일어설 용기를 얻는다.`,
    choices: [
      {
        text: '힘을 모은 마을의 응원을 뒤로하고 산맥으로 향한다.',
        next: 'mountainPass',
      },
    ],
  },
  mountainPass: {
    description: (ctx) => {
      const allies = ctx.alliedRangers
        ? '숲의 순찰대가 그림자 속에서 활을 겨누며 뒤를 지킨다.'
        : '홀로 맞서는 길이지만, 마음만은 흔들리지 않는다.';
      const relic = ctx.sacredRelic
        ? '손에 쥔 성배는 은은한 빛을 내뿜으며 용의 마법을 봉인할 준비를 한다.'
        : '손에는 검 한 자루뿐, 오직 용기의 힘에 의지해야 한다.';
      return `바람이 매서운 산악 길목에서 ${ctx.heroName}는 마지막 결전을 앞둔다. ${allies} ${relic}`;
    },
    choices: [
      {
        text: '용의 보금자리로 돌격해 결전을 벌인다.',
        next: 'dragonLair',
      },
      {
        text: '용에게 대화를 제안해 피를 흘리지 않는 길을 모색한다.',
        next: 'dragonParley',
      },
    ],
  },
  dragonParley: {
    description: (ctx) => {
      if (ctx.sacredRelic) {
        return `용은 성배에서 뿜어져 나오는 빛에 눈을 가늘게 뜨더니, ${ctx.heroName}의 목소리를 듣고는 마침내 협상에 응한다. 왕국은 성배를 봉인으로 삼고 용과 공존의 서약을 맺는다.`;
      }
      if (ctx.alliedRangers || ctx.villageInspired) {
        return `용은 처음에는 포효했지만, ${ctx.heroName}와 그 뒤에 선 이들의 굳건한 연대에 마음을 누그러뜨린다. 긴 협상 끝에 용은 더 이상 왕국을 괴롭히지 않겠다고 약속한다.`;
      }
      return `${ctx.heroName}의 말에도 용은 포악한 기세를 거두지 않는다. 협상은 실패했고, 불꽃이 하늘을 가른다. 살아남기 위해서는 싸워야 한다.`;
    },
    choices: (ctx) => {
      if (!ctx.sacredRelic && !ctx.alliedRangers && !ctx.villageInspired) {
        return [
          {
            text: '어쩔 수 없다. 검을 뽑아 전투를 시작한다.',
            next: 'dragonLair',
          },
        ];
      }
      return [
        {
          text: '왕국으로 돌아가 평화 협약을 전한다.',
          next: 'epiloguePeace',
        },
      ];
    },
  },
  dragonLair: {
    description: (ctx) => {
      const support = ctx.alliedRangers
        ? '순찰대의 화살이 하늘을 가르며 용의 날개를 묶는다.'
        : '외로운 싸움이지만, 두려움을 넘어서야 한다.';
      if (ctx.sacredRelic) {
        return `${ctx.heroName}는 성배를 들어 올려 봉인의 문구를 외친다. ${support} 눈부신 빛이 폭발하며 용의 불꽃을 잠재운다.`;
      }
      if (ctx.villageInspired) {
        return `${ctx.heroName}는 마을 사람들의 응원을 떠올리며 마지막 힘을 짜낸다. ${support} 길고 치열한 전투 끝에 용은 패배를 인정하고 날개를 접는다.`;
      }
      return `용의 불꽃은 대지를 붉게 물들인다. ${ctx.heroName}는 끝까지 맞섰지만, 봉인도 지원도 없이 압도적인 힘에 쓰러지고 만다.`;
    },
    choices: (ctx) => {
      if (!ctx.sacredRelic && !ctx.villageInspired) {
        return [
          {
            text: '용사의 전설은 이렇게 끝났다. 다시 도전한다.',
            next: 'restart',
          },
        ];
      }
      return [
        {
          text: '승리를 거머쥔 채 왕국으로 귀환한다.',
          next: 'epilogueVictory',
        },
      ];
    },
  },
  epiloguePeace: {
    description: (ctx) =>
      `${ctx.heroName}의 이름은 평화의 중재자로 길이 남게 되었다. 왕국과 용은 서로의 영토를 존중하며 번영을 나누게 된다.`,
    choices: [
      {
        text: '새로운 모험을 향해 떠난다.',
        next: 'restart',
      },
    ],
  },
  epilogueVictory: {
    description: (ctx) =>
      `${ctx.heroName}는 왕궁의 성문 앞에서 영웅의 환호를 받는다. 용의 위협이 사라진 왕국은 다시금 풍요로워지고, 전설은 대대로 전해진다.`,
    choices: [
      {
        text: '다른 선택을 해 본다.',
        next: 'restart',
      },
    ],
  },
};

const restartScene = {
  description: () =>
    '이야기는 다시 시작될 준비가 되었다. 이번에는 어떤 운명을 그리게 될까?',
  choices: [
    {
      text: '새로운 이름으로 모험을 다시 시작한다.',
      next: 'restartName',
    },
    {
      text: '같은 이름으로 여정을 이어 간다.',
      next: 'restartSameName',
    },
  ],
};

function renderScene(sceneId) {
  if (sceneId === 'restart') {
    renderSceneData(restartScene);
    return;
  }

  if (sceneId === 'restartName') {
    resetState(true);
    return;
  }

  if (sceneId === 'restartSameName') {
    resetState();
    return;
  }

  const scene = scenes[sceneId];
  if (!scene) {
    storyLog.textContent = '알 수 없는 갈림길에 도달했습니다.';
    choiceList.innerHTML = '';
    return;
  }
  renderSceneData(scene);
}

function renderSceneData(scene) {
  const description =
    typeof scene.description === 'function'
      ? scene.description(state)
      : scene.description;

  storyLog.textContent = description;

  const choices =
    typeof scene.choices === 'function' ? scene.choices(state) : scene.choices;

  choiceList.innerHTML = '';

  choices.forEach((choice) => {
    const button = document.createElement('button');
    button.className = 'choice-button';
    button.type = 'button';
    button.textContent = choice.text;
    button.addEventListener('click', () => {
      if (typeof choice.effect === 'function') {
        choice.effect(state);
      }
      renderScene(choice.next);
    });
    choiceList.appendChild(button);
  });
}

function resetState(showNamePrompt = false) {
  state.alliedRangers = false;
  state.sacredRelic = false;
  state.villageInspired = false;

  if (showNamePrompt) {
    state.heroName = '';
    nameScreen.classList.remove('hidden');
    storyScreen.classList.add('hidden');
    storyLog.textContent = '';
    choiceList.innerHTML = '';
    document.getElementById('hero-name').focus();
    return;
  }

  renderScene('village');
}

nameForm.addEventListener('submit', (event) => {
  event.preventDefault();
  const input = new FormData(event.target).get('hero-name');
  const trimmed = (input || '').trim();
  if (!trimmed) {
    return;
  }
  state.heroName = trimmed;
  resetState();
  nameScreen.classList.add('hidden');
  storyScreen.classList.remove('hidden');
});

// 키보드 접근성을 위한 기본 포커스 처리
window.addEventListener('load', () => {
  document.getElementById('hero-name').focus();
});
