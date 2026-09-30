/**
 * Device Capability Detection
 * Checks for hardware acceleration and browser support for edge AI.
 */
export const checkCapabilities = () => {
  const capabilities = {
    hasWebGPU: false,
    hasWebGL: false,
    hasCamera: false,
    memoryEstimate: 'unknown'
  }

  // Check WebGPU (future-proofing)
  if ('gpu' in navigator) {
    capabilities.hasWebGPU = true
  }

  // Check WebGL (current ONNX fallback)
  try {
    const canvas = document.createElement('canvas')
    capabilities.hasWebGL = !!(window.WebGLRenderingContext && (canvas.getContext('webgl') || canvas.getContext('experimental-webgl')))
  } catch (e) {
    capabilities.hasWebGL = false
  }

  // Check Media Devices
  if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    capabilities.hasCamera = true
  }

  // Check device memory (rough estimate in GB)
  if ('deviceMemory' in navigator) {
    capabilities.memoryEstimate = navigator.deviceMemory
  }

  return capabilities
}
