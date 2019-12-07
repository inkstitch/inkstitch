<template>
  <div ref="simulator" class="simulator vld-parent">
    <fieldset>
      <div class="window-controls">
        <div ref="controlInfoButton" class="control-info-button" v-on:click="toggleInfo">
          <font-awesome-icon icon="info"/>
          <collapse-transition>
            <div class="control-info" v-show="infoExpanded" v-bind:style="{'max-height': infoMaxHeight + 'px'}">
              <h1>
                <font-awesome-icon icon="info" class="info-icon"/>
                <translate>Simulator Shortcut Keys</translate>
              </h1>
              <div>
                <div>
                  <p>
                    <translate>Button</translate>
                  </p>
                  <p>
                    <translate>Function</translate>
                  </p>
                  <p>
                    <translate>Shortcut Key</translate>
                  </p>
                </div>
                <div>
                  <p>
                    <font-awesome-icon icon="pause" class="fa-button"/>
                  </p>
                  <p>
                    <translate>Pause</translate>
                  </p>
                  <p>
                    <translate>Space</translate>
                  </p>
                </div>
                <div>
                  <p>
                    <font-awesome-icon icon="play" class="fa-button"/>
                  </p>
                  <p>
                    <translate>Play</translate>
                  </p>
                  <p>P</p>
                </div>
                <div>
                  <p>
                    <font-awesome-icon icon="angle-double-left" class="fa-button"/>
                  </p>
                  <p>
                    <translate>Play backward</translate>
                  </p>
                  <p>
                    <translate translate-comment="name for left arrow keyboard key">← Arrow left</translate>
                  </p>
                </div>
                <div>
                  <p>
                    <font-awesome-icon icon="angle-double-right" class="fa-button"/>
                  </p>
                  <p>
                    <translate>Play forward</translate>
                  </p>
                  <p>
                    <translate translate-comment="name for right arrow keyboard key">→ Arrow right</translate>
                  </p>
                </div>
                <div>
                  <p>
                    <font-awesome-icon icon="shoe-prints" class="fa-button fa-flip-horizontal"/>
                  </p>
                  <p>
                    <translate translate-comment="description of keyboard shortcut that moves one stitch backward in simulator">
                      One step backward
                    </translate>
                  </p>
                  <p>-
                    <translate translate-comment="name for this keyboard key: -">Minus</translate>
                  </p>
                </div>
                <div>
                  <p>
                    <font-awesome-icon icon="shoe-prints" class="fa-button"/>
                  </p>
                  <p>
                    <translate translate-comment="description of keyboard shortcut that moves one stitch forward in simulator">
                      One step forward
                    </translate>
                  </p>
                  <p>
                    <translate translate-comment="name for this keyboard key: +">+ Plus</translate>
                  </p>
                </div>
                <div>
                  <p>
                    <font-awesome-icon icon="step-backward" class="fa-button"/>
                  </p>
                  <p>
                    <translate>Jump to previous command</translate>
                  </p>
                  <p><translate translate-comment="name for page down keyboard key">Page down (PgDn)</translate></p>
                </div>
                <div>
                  <p>
                    <font-awesome-icon icon="step-forward" class="fa-button"/>
                  </p>
                  <p>
                    <translate>Jump to next command</translate>
                  </p>
                  <p><translate translate-comment="name for page up keyboard key">Page up (PgUp)</translate></p>
                </div>
                <div>
                  <p>
                    <font-awesome-icon icon="hippo" class="fa-button"/>
                  </p>
                  <p>
                    <translate>Slow down</translate>
                  </p>
                  <p>
                    <translate translate-comment="name for down arrow keyboard key">↓ Arrow down</translate>
                  </p>
                </div>
                <div>
                  <p>
                    <font-awesome-icon icon="horse" class="fa-button"/>
                  </p>
                  <p>
                    <translate>Speed up</translate>
                  </p>
                  <p>
                    <translate translate-comment="name for up arrow keyboard key">↑ Arrow up</translate>
                  </p>
                </div>
              </div>
            </div>
          </collapse-transition>
        </div>
        <div class="toggle-controls" v-on:click="toggleControls">
          <font-awesome-icon v-if="controlsExpanded" icon="minus"/>
          <font-awesome-icon v-else icon="plus"/>
        </div>
      </div>
      <collapse-transition>
        <div class="panel" v-show="controlsExpanded">
          <fieldset class="controls">
            <legend>
              <translate>Controls</translate>
            </legend>
            <button v-on:click="stop" :class="{pressed: paused}" :title="$gettext('Pause (space)')">
              <font-awesome-icon icon="pause" size="2x" class="fa-button"/>
            </button>
            <button v-on:click="start" :class="{pressed: animating}" :title="$gettext('Play (arrow left | arrow right)')">
              <font-awesome-icon icon="play" size="2x" class="fa-button"/>
            </button>
            <button v-on:click="animationReverse" :class="{pressed: reverse}" :title="$gettext('Play backward (arrow left)')">
              <font-awesome-icon icon="angle-double-left" size="2x" class="fa-button" :mask="['fas', 'stop']"/>
            </button>
            <button v-on:click="animationForward" :class="{pressed: forward}" :title="$gettext('Play forward (arrow right)')">
              <font-awesome-icon icon="angle-double-right" size="2x" class="fa-button" :mask="['fas', 'stop']"/>
            </button>
            <button v-on:click="animationBackwardOneStitch" :title="$gettext('One step backward (-)')">
              <font-awesome-icon icon="shoe-prints" size="2x" class="fa-button fa-flip-horizontal"/>
            </button>
            <button v-on:click="animationForwardOneStitch" :title="$gettext('One step forward (+)')">
              <font-awesome-icon icon="shoe-prints" size="2x" class="fa-button"/>
            </button>
            <button v-on:click="animationPreviousCommand" :title="$gettext('Jump to previous command (Page down)')">
              <font-awesome-icon icon="step-backward" size="2x" class="fa-button"/>
            </button>
            <button v-on:click="animationNextCommand" :title="$gettext('Jump to next command (Page up)')">
              <font-awesome-icon icon="step-forward" size="2x" class="fa-button"/>
            </button>
          </fieldset>
          <fieldset class="speed">
            <legend>
              <translate :translate-n="speed" translate-plural="Speed: %{speed} stitches/sec">Speed: %{speed} stitch/sec</translate>
            </legend>
            <button v-on:click="animationSlowDown" :title="$gettext('Slow down (arrow down)')">
              <font-awesome-icon icon="hippo" size="2x" class="fa-button"/>
            </button>
            <button v-on:click="animationSpeedUp" :title="$gettext('Speed up (arrow up)')">
              <font-awesome-icon icon="align-right" class="fa-motion-lines"/>
              <font-awesome-icon icon="horse" size="2x" class="fa-button fa-fast"/>
            </button>
          </fieldset>
          <fieldset class="command">
            <legend>
              <translate>Command</translate>
            </legend>
            <span class="current-command">{{currentCommand}}</span>
          </fieldset>
          <fieldset class="show-commands">
            <legend>Show</legend>
            <span>
              <input id="trim-checkbox" type="checkbox" v-model="showTrims"/>
              <label for="trim-checkbox"><font-awesome-icon icon="cut"/> <translate>trims</translate></label>
              <br/>
              <input id="jump-checkbox" type="checkbox" v-model="showJumps"/>
              <label for="jump-checkbox"><font-awesome-icon icon="frog"/> <translate>jumps</translate></label>
            </span>
            <span>
              <input id="color-change-checkbox" type="checkbox" v-model="showColorChanges"/>
              <label for="color-change-checkbox"><font-awesome-icon icon="exchange-alt"/> <translate>color changes</translate></label>
              <br/>
              <input id="stop-checkbox" type="checkbox" v-model="showStops"/>
              <label for="stop-checkbox"><font-awesome-icon icon="pause"/> <translate>stops</translate></label>
            </span>
            <span class="npp">
            <input id="npp-checkbox" type="checkbox" v-model="showNeedlePenetrationPoints"/>
            <label for="npp-checkbox">
              <font-awesome-layers>
                <font-awesome-icon icon="circle" transform="shrink-9"/>
                <font-awesome-icon icon="minus" class="fa-thin-line"/>
              </font-awesome-layers>
              <span v-translate>needle<br/>points</span>
            </label>
          </span>
          </fieldset>
        </div>
      </collapse-transition>
      <div class="slider-container">
        <span>1</span>
        <span class="slider-box">
          <vue-slider
              :value="currentStitchDisplay"
              @change="setCurrentStitch"
              :min="0"
              :max="numStitches"
              :duration="0"
              :marks="sliderMarks"
              :process="sliderProcess">
            <template v-slot:label="mark">
              <div :class="['vue-slider-mark-label', `slider-label-${mark.command}`, { active: mark.active }]">
                <font-awesome-icon :icon="mark.icon"/>
              </div>
            </template>
          </vue-slider>
        </span>
        <span>{{numStitches}}</span>
        <input ref="currentStitchInput"
               class="current-stitch-input"
               :value="currentStitchDisplay"
               @change="onCurrentStitchEntered"
               @focus="stop"/>
      </div>
    </fieldset>
    <loading :active.sync="loading" :is-full-page="false">
      <div class="loading">
        <div class="loading-icon">
          <font-awesome-icon icon="spinner" size="4x" pulse/>
        </div>
        <div class="loading-text">
          <translate>Rendering stitch-plan...</translate>
        </div>
      </div>
    </loading>
  </div>
</template>

<script src="../assets/js/simulator.js"></script>

<style src="../assets/style/simulator.css" scoped></style>
