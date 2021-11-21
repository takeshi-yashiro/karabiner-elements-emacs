#
# Emacs Keybindings for Karabiner Elements
#
# 利用方法:
#  1. Karabiner Elements をインストール
#  2. Simple modifications で right_command を right_option にマップ
#  3. python3 emacskeys.py > ~/.config/karabiner/assets/complex_modifications/myemacs.json
#  4. Karabiner Elements の Complex modifications に追加された "Emacs key bindings (yashiro)" を Enable する
# 


import json

cond_disable = {
  "type": "frontmost_application_unless",
  "bundle_identifiers": [
    "^org\\.gnu\\.Emacs$",
    "^org\\.gnu\\.AquamacsEmacs$",
    "^org\\.gnu\\.Aquamacs$",
    "^org\\.pqrs\\.unknownapp.conkeror$",
    "^com\\.microsoft\\.rdc$",
    "^com\\.microsoft\\.rdc\\.",
    "^net\\.sf\\.cord$",
    "^com\\.thinomenon\\.RemoteDesktopConnection$",
    "^com\\.itap-mobile\\.qmote$",
    "^com\\.nulana\\.remotixmac$",
    "^com\\.p5sys\\.jump\\.mac\\.viewer$",
    "^com\\.p5sys\\.jump\\.mac\\.viewer\\.",
    "^com\\.teamviewer\\.TeamViewer$",
    "^com\\.vmware\\.horizon$",
    "^com\\.2X\\.Client\\.Mac$",
    "^com\\.apple\\.Terminal$",
    "^com\\.googlecode\\.iterm2$",
    "^co\\.zeit\\.hyperterm$",
    "^co\\.zeit\\.hyper$",
    "^io\\.alacritty$",
    "^net\\.kovidgoyal\\.kitty$",
    "^org\\.vim\\.",
    "^com\\.qvacua\\.VimR$",
    "^com\\.vmware\\.fusion$",
    "^com\\.vmware\\.horizon$",
    "^com\\.vmware\\.view$",
    "^com\\.parallels\\.desktop$",
    "^com\\.parallels\\.vm$",
    "^com\\.parallels\\.desktop\\.console$",
    "^org\\.virtualbox\\.app\\.VirtualBoxVM$",
    "^com\\.citrix\\.XenAppViewer$",
    "^com\\.vmware\\.proxyApp\\.",
    "^com\\.parallels\\.winapp\\.",
    "^org\\.x\\.X11$",
    "^com\\.apple\\.x11$",
    "^org\\.macosforge\\.xquartz\\.X11$",
    "^org\\.macports\\.X11$",
    "^com\\.sublimetext\\.",
    "^com\\.microsoft\\.VSCode$"
  ]
}

set_spc = {
  "set_variable": {
    "name": "C-SPC",
    "value": 1
  }
}
clear_spc = {
  "set_variable": {
    "name": "C-SPC",
    "value": 0
  }
}

def cmd(src, dst, src_modifiers=["control"], src_modifiers_opt=["caps_lock"], dst_modifiers=["left_command"]):
  data = {
    "type": "basic",
    "from": {
      "key_code": src,
      "modifiers": {
        # "mandatory": src_modifiers,
        # "optional": src_modifiers_opt
      }
    },
    "to": [
      {
      }
    ],
    "conditions": [cond_disable]
  }
  if dst is not None:
    data["to"] = [{
      "key_code": dst,
      #"modifiers": dst_modifiers
    }]
    if dst_modifiers is not None:
      data["to"][0]["modifiers"] = dst_modifiers

  if src_modifiers is not None:
    data["from"]["modifiers"]["mandatory"] = src_modifiers
  if src_modifiers_opt is not None:
    data["from"]["modifiers"]["optional"] = src_modifiers_opt
  return data

# C-x
def ctrl_x_cmd(src, dst, src_modifiers=["control"], src_modifiers_opt=["caps_lock"], dst_modifiers=["left_command"]):
  data = cmd(src, dst, src_modifiers=src_modifiers, src_modifiers_opt=src_modifiers_opt, dst_modifiers=dst_modifiers)
  data["conditions"].append({
    "type": "variable_if",
    "name": "C-x",
    "value": 1
  })
  data["to"].append(clear_spc)
  return data

# C-SPCを無視するコマンド
def normal_cmd(src, dst, clear_space=True, src_modifiers=["control"], src_modifiers_opt=["caps_lock"], dst_modifiers=["left_command"]):
  data = cmd(src, dst, src_modifiers=src_modifiers, src_modifiers_opt=src_modifiers_opt, dst_modifiers=dst_modifiers)
  data["conditions"].append({
    "type": "variable_unless",
    "name": "C-x",
    "value": 1
  })
  if clear_space:
    data["to"].append(clear_spc)
  return data

# 移動系のコマンド (C-SPCに基づき処理)
def move_cmds(src, dst, src_modifiers=["control"], src_modifiers_opt=["caps_lock", "shift"], dst_modifiers=["left_command"]):
  # SPACEが押されていないときはそのまま
  nospc = normal_cmd(src, dst, clear_space=False, src_modifiers=src_modifiers, src_modifiers_opt=src_modifiers_opt, dst_modifiers=dst_modifiers)
  nospc["conditions"].append({
    "type": "variable_unless",
    "name": "C-SPC",
    "value": 1
  })

  # SPACEが押されているときは、Shiftを追加
  if dst_modifiers is None:
    dst_modifiers = []
  dst_modifiers.append("left_shift")
  spc = normal_cmd(src, dst, clear_space=False, src_modifiers=src_modifiers, src_modifiers_opt=src_modifiers_opt, dst_modifiers=dst_modifiers)
  spc["conditions"].append({
    "type": "variable_if",
    "name": "C-SPC",
    "value": 1
  })

  return [nospc, spc]

# --------

manipulators = []

# C-x C-f, C-f
manipulators.append(ctrl_x_cmd("f", "o"))
manipulators.extend(move_cmds("f", "right_arrow", dst_modifiers=None))

# C-x C-c
manipulators.append(ctrl_x_cmd("c", "q"))

# C-d
manipulators.append(normal_cmd("d", "delete_forward", dst_modifiers=None))

# C-h
manipulators.append(normal_cmd("h", "delete_or_backspace", dst_modifiers=None))

# C-k
c = normal_cmd("k", "end", dst_modifiers=["left_shift"])
c["to"].append({"key_code": "x", "modifiers": "left_command"})
manipulators.append(c)

# C-o
c = normal_cmd("o", "end", dst_modifiers=None)
c["to"].append({"key_code": "end"})
c["to"].append({"key_code": "up_arrow"})
manipulators.append(c)

# C-g
manipulators.append(normal_cmd("g", "escape", dst_modifiers=None))

# C-j
c = normal_cmd("j", "return_or_enter", dst_modifiers=None)
c["to"].append({"key_code": "tab"})
manipulators.append(c)

# C-m
manipulators.append(normal_cmd("m", "return_or_enter", dst_modifiers=None))

# C-i
manipulators.append(normal_cmd("m", "tab", dst_modifiers=None))

# C-x C-s, C-s
manipulators.append(ctrl_x_cmd("s", "s"))
manipulators.append(normal_cmd("s", "f"))

# C-r
manipulators.append(normal_cmd("r", "f"))

# C-w
manipulators.append(normal_cmd("w", "x"))

# M-w
manipulators.append(normal_cmd("w", "c", src_modifiers=["option"]))

# C-y
manipulators.append(normal_cmd("y", "v"))

# C-/
manipulators.append(normal_cmd("slash", "z"))

# C-a
manipulators.extend(move_cmds("a", "home", dst_modifiers=None))

# C-e
manipulators.extend(move_cmds("e", "end", dst_modifiers=None))

# C-p
manipulators.extend(move_cmds("p", "up_arrow", dst_modifiers=None))

# C-n
manipulators.extend(move_cmds("n", "down_arrow", dst_modifiers=None))

# C-b
manipulators.extend(move_cmds("b", "left_arrow", dst_modifiers=None))

# C-v
manipulators.extend(move_cmds("v", "page_down", dst_modifiers=None))

# M-v
manipulators.extend(move_cmds("v", "page_up", src_modifiers=["option"], dst_modifiers=None))

# C-x h
manipulators.append(ctrl_x_cmd("h", "a", src_modifiers=None))

# C-x k
manipulators.append(ctrl_x_cmd("k", "w", src_modifiers=None))

# C-@, C-SPCを兼用
for kc in ["spacebar", "open_bracket"]:
  c = normal_cmd(kc, None, clear_space=False)
  c["to"] = [{
    "set_variable": {
    "name": "C-SPC",
    "value": 1
    }
  }]
  c["conditions"].append({
    "type": "variable_unless",
    "name": "C-SPC",
    "value": 1
  })
  manipulators.append(c)

  # (マーク開始後に C-SPC した場合はそれまでの選択をキャンセルする)
  c = normal_cmd(kc, "escape", clear_space=False, dst_modifiers=None)
  c["conditions"].append({
    "type": "variable_if",
    "name": "C-SPC",
    "value": 1
  })
  manipulators.append(c)

# C-x
manipulators.append({
  "type": "basic",
  "from": {
    "any": "key_code",
    "modifiers": {
      "optional": [
        "any"
      ]
    }
  },
  "conditions": [
    {
      "type": "variable_if",
      "name": "C-x",
      "value": 1
    }
  ]
  # 何も送らずに C-x 以降の命令を捨てている
})
manipulators.append({
  "type": "basic",
  "from": {
    "key_code": "x",
    "modifiers": {
      "mandatory": [
        "control"
      ],
      "optional": [
        "caps_lock"
      ]
    }
  },
  "to": [
    {
      "set_variable": {
        "name": "C-x",
        "value": 1
      }
    }
  ],
  "to_delayed_action": {
    "to_if_invoked": [
      {
        "set_variable": {
          "name": "C-x",
          "value": 0
        }
      }
    ],
    "to_if_canceled": [
      {
        "set_variable": {
          "name": "C-x",
          "value": 0
        }
      }
    ]
  },
  "conditions": [cond_disable]
})

# S-SPC: Toggle Eisu
manipulators.append({
  "type": "basic",
  "from": {
    "key_code": "spacebar",
    "modifiers": { "mandatory": ["left_shift"], "optional": ["caps_lock"] }
  },
  "conditions": [
    {
      "type": "input_source_if",
      "input_sources": [
        { "language": "en" }
      ]
    }
  ],
  "to": [{ "key_code": "japanese_kana" }]
})
manipulators.append({
  "type": "basic",
  "from": {
    "key_code": "spacebar",
    "modifiers": { "mandatory": ["left_shift"], "optional": ["caps_lock"] }
  },
  "conditions": [
    {
      "type": "input_source_if",
      "input_sources": [
        { "language": "ja" }
      ]
    }
  ],
  "to": [{ "key_code": "japanese_eisuu" }]
})

# C-SPC -> C-@
manipulators.append({
  "type": "basic",
  "from": {
    "key_code": "spacebar",
    "modifiers": { "mandatory": ["control"], "optional": ["caps_lock"] }
  },
  "to": [{
    "key_code": "open_bracket",
    "modifiers": ["left_control"]
  }]
})

# C-~ -> Spotlight
manipulators.append({
  "type": "basic",
  "from": {
    "key_code": "equal_sign",
    "modifiers": { "mandatory": ["control"], "optional": ["caps_lock"] }
  },
  "to": [{
    "key_code": "spacebar",
    "modifiers": ["left_command"]
  }]
})

# C-t, C-z (Emacsキーバインドではないがそのままマップ)
for kc in ["t", "z"]:
  manipulators.append(normal_cmd(kc, kc))

# C-z (for VSCode only)
c = normal_cmd("z", "slash", dst_modifiers=["left_control"])
c["conditions"] = [{
  "type": "frontmost_application_if",
  "bundle_identifiers": [
    "^com\\.microsoft\\.VSCode$"
  ]
}]
manipulators.append(c)

# Right-Option + Tab (Switch window)
# - Simple Modifications で right_command を right_option に remap している前提
manipulators.append({
  "type": "basic",
  "from": {
    "key_code": "tab",
    "modifiers": { "mandatory": ["option"] }
  },
  "to": [{
    "key_code": "tab",
    "modifiers": ["right_command"]
  }]
})
manipulators.append({
  "type": "basic",
  "from": {
    "key_code": "tab",
    "modifiers": { "mandatory": ["option", "shift"] }
  },
  "to": [{
    "key_code": "tab",
    "modifiers": ["right_command"]
  }]
})

# Final result
output = {
  "title": "Emacs key bindings (yashiro)",
  "maintainers": [
    "yashiro"
  ],
  "rules": [
    {
      "description": "Emacs key bindings (yashiro)",
      "manipulators": manipulators
    }
  ]
}

print(json.dumps(output, indent=2))