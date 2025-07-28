# Undertale-Style Combat Game

A Python + Pygame implementation of Undertale-style turn-based combat with bullet hell dodging mechanics.

## Features

- **Turn-based Combat**: Choose from Fight, Act, Item, or Mercy options
- **Bullet Hell Dodging**: Control your soul (red heart) to dodge various bullet patterns
- **Multiple Attack Patterns**: Rain, spiral, cross, and scatter attack patterns
- **Health System**: Player and enemy HP with visual health bars
- **Invincibility Frames**: Brief invincibility after taking damage
- **Victory Conditions**: Defeat enemies by fighting or show mercy when they're weak

## Installation

1. Make sure you have Python 3.7+ installed
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## How to Play

1. Run the game:
```bash
python main.py
```

2. **Main Menu**: Press SPACE to start combat

3. **Player Turn**: 
   - Use LEFT/RIGHT arrow keys to select an action
   - Press Z or ENTER to confirm your choice
   - **FIGHT**: Deal damage to the enemy
   - **ACT**: Try to reason with the enemy
   - **ITEM**: Heal yourself
   - **MERCY**: Spare the enemy (only works when they're weak)

4. **Enemy Turn (Dodge Phase)**:
   - Use WASD or arrow keys to move your heart
   - Avoid the colored bullets!
   - Different enemies have different attack patterns

5. **Win Conditions**:
   - Defeat the enemy by reducing their HP to 0
   - OR spare them when their HP is low (below 30%)

## Controls

### Menu Navigation
- **Arrow Keys**: Navigate menus
- **Z/Enter**: Confirm selection
- **ESC**: Quit (on game over screen)

### Dodging Phase
- **WASD** or **Arrow Keys**: Move your soul to dodge bullets
- Stay within the white combat box!

## Customization Ideas

### Easy Modifications
- Change colors in `settings.py`
- Adjust player speed, damage, or HP
- Modify attack patterns in `enemy.py`
- Add new bullet patterns in `attacks/bullet_patterns.py`

### Advanced Features to Add
- **Multiple Enemies**: Create different enemy types with unique patterns
- **Sound Effects**: Add audio feedback for attacks, damage, menu navigation
- **Sprites**: Replace colored rectangles with actual sprite art
- **Story Elements**: Add dialogue and narrative between fights
- **Save System**: Implement game progress saving
- **More Attack Types**: Lasers, homing missiles, wall patterns
- **Power-ups**: Temporary speed boosts, shields, etc.
- **Difficulty Scaling**: Enemies get harder over time

## Technical Details

- **Engine**: Pygame 2.5.2
- **Python Version**: 3.7+
- **Target FPS**: 60 FPS
- **Resolution**: 800x600 (configurable in settings.py)

## Development Roadmap
1. ✅ Basic combat system
2. ✅ Player movement and dodging
3. ✅ Multiple attack patterns
4. ✅ Health system and UI
5. 🔄 Sound effects and music
6. 🔄 Sprite graphics
7. 🔄 Multiple enemy types
8. 🔄 Story mode
9. 🔄 Save system
10. 🔄 Polish and effects

## Contributing
- New bullet patterns
- Enemy types
- Visual effects
- Sound design
- UI improvements
